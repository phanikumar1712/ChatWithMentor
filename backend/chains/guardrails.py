"""
NeMo Guardrails integration for the AI Mentors backend.

Design decisions:
- Fail-open: if the rails engine fails to initialize or errors at runtime,
  we log and allow the message through. Availability beats a hard dependency
  on a safety pre-check (the mentor prompts already contain a safety layer).
- Environment flags:
    GUARDRAILS_ENABLED  (default "true")
    GUARDRAILS_TIMEOUT  (default "10", seconds)
- Reuses the OpenRouter LLM so self-check rails use the same provider.
"""

import asyncio
import logging
import os
from typing import Optional

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

logger = logging.getLogger("ai_mentor.guardrails")

# NeMo's colang runtime logs every internal event at INFO — far too noisy.
logging.getLogger("nemoguardrails").setLevel(logging.WARNING)

GUARDRAILS_ENABLED = os.getenv("GUARDRAILS_ENABLED", "true").lower() != "false"
GUARDRAILS_TIMEOUT = float(os.getenv("GUARDRAILS_TIMEOUT", "10"))

_rails = None
_init_attempted = False


def _build_llm() -> Optional[ChatOpenAI]:
    """Same provider/settings as mentor_chain.llm so rails stay consistent."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        logger.warning(
            "OPENAI_API_KEY not set — self-check rails need an LLM. "
            "Guardrails disabled (fail-open)."
        )
        return None

    kwargs = dict(
        model=os.getenv("OPENAI_MODEL", "openai/gpt-3.5-turbo"),
        openai_api_key=api_key,
        temperature=0.0,  # self-check rails should be deterministic
        default_headers={
            "HTTP-Referer": "http://localhost:5173",
            "X-Title": "AI Mentors App",
        },
    )
    api_base = os.getenv("OPENAI_API_BASE")
    if api_base:
        kwargs["openai_api_base"] = api_base
    return ChatOpenAI(**kwargs)


def _get_rails():
    """Lazily initialize the rails engine once. Returns None on failure (fail-open)."""
    global _rails, _init_attempted

    if _rails is not None or _init_attempted:
        return _rails

    _init_attempted = True
    try:
        from nemoguardrails import LLMRails, RailsConfig

        llm = _build_llm()
        if llm is None:
            return None

        config_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "config",
            "guardrails",
        )
        config = RailsConfig.from_path(config_path)

        from nemoguardrails.integrations.langchain.llm_adapter import LangChainLLMAdapter

        _rails = LLMRails(config, llm=LangChainLLMAdapter(llm))
        logger.info("NeMo Guardrails initialized from %s", config_path)
    except Exception:
        logger.exception("Failed to initialize NeMo Guardrails — rails disabled (fail-open)")
        _rails = None

    return _rails


def _rail_type(rail_type: str):
    """Convert 'input'/'output' to the RailType enum check_async expects."""
    from nemoguardrails.rails.llm.options import RailType

    return RailType.OUTPUT if rail_type == "output" else RailType.INPUT


async def _run_check(messages: list, rail_type: str) -> Optional[dict]:
    """
    Run a check with the rails engine.

    Returns:
        None               -> rails disabled, not initialized, errored, or timed out (allow)
        {"blocked": ..., "content": ...} -> rails ran successfully
    """
    if not GUARDRAILS_ENABLED:
        return None

    rails = _get_rails()
    if rails is None:
        return None

    try:
        result = await asyncio.wait_for(
            rails.check_async(messages=messages, rail_types=[_rail_type(rail_type)]),
            timeout=GUARDRAILS_TIMEOUT,
        )
    except asyncio.TimeoutError:
        logger.warning("Guardrails %s check timed out after %ss — allowing (fail-open)",
                       rail_type, GUARDRAILS_TIMEOUT)
        return None
    except Exception:
        logger.exception("Guardrails %s check failed — allowing (fail-open)", rail_type)
        return None

    return {
        "blocked": getattr(result, "status", "") == "blocked",
        "content": getattr(result, "content", None),
    }


async def check_input(user_message: str) -> Optional[str]:
    """
    Run input rails on the user message.

    Returns a canned refusal string if the message is blocked, else None to allow.
    """
    result = await _run_check([{"role": "user", "content": user_message}], "input")
    if result and result["blocked"]:
        return (
            "I'm sorry, I can't respond to that. Let's keep our conversation "
            "respectful and positive."
        )
    return None


async def check_output(mentor_reply: str) -> Optional[str]:
    """
    Run output rails on the mentor's reply.

    Returns a safe replacement string if the reply is blocked, else None to allow.
    """
    result = await _run_check([{"role": "assistant", "content": mentor_reply}], "output")
    if result and result["blocked"]:
        return (
            "I'd rather not share that. Is there something else I can help you with?"
        )
    return None

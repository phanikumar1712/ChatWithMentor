"""
Guardrails test suite for the AI Mentors backend.

Run from backend/:   ./venv/bin/python tests/test_guardrails.py

Uses a scripted fake LLM (no real API key needed):
- prompt contains "should be blocked"  -> answers "Yes"  -> rail blocks
- otherwise                            -> answers "No"   -> rail allows
"""

import asyncio
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langchain_core.messages import AIMessage  # noqa: E402
from nemoguardrails import LLMRails, RailsConfig  # noqa: E402

from chains import guardrails as g  # noqa: E402

PASS, FAIL = "✅ PASS", "❌ FAIL"
results = []


def record(name, ok, extra=""):
    results.append((name, ok))
    print(f"{PASS if ok else FAIL}  {name}" + (f"  ({extra})" if extra else ""))


# ---------------------------------------------------------------------------
# Fake LLM: decides Yes/No based on keywords in the rendered prompt.
# The rendered self-check prompt includes the full policy + the message.
# ---------------------------------------------------------------------------
class ScriptedLLM:
    def __init__(self):
        self.last_prompt = None

    def bind(self, **kwargs):
        return self

    async def ainvoke(self, messages, **kwargs):
        # The adapter may pass a plain string prompt or a list of messages
        if isinstance(messages, str):
            text = messages
        else:
            text = "\n".join(
                m.content if hasattr(m, "content") else str(m) for m in messages
            )
        self.last_prompt = text
        blocked = "BLOCKED_MARKER" in text or "banned_word" in text
        return AIMessage(content="Yes" if blocked else "No")


FAKE = ScriptedLLM()


def build_fresh_rails():
    from nemoguardrails.integrations.langchain.llm_adapter import LangChainLLMAdapter

    config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                               "config", "guardrails")
    config = RailsConfig.from_path(config_path)
    return LLMRails(config, llm=LangChainLLMAdapter(FAKE))


# ---------------------------------------------------------------------------
# Unit tests: check_input / check_output
# ---------------------------------------------------------------------------
async def unit_tests():
    print("\n=== UNIT: check_input / check_output (scripted LLM) ===")

    # 1. Safe message allowed
    g._rails = build_fresh_rails()
    g._init_attempted = True
    res = await g.check_input("What is my dharma?")
    record("check_input allows safe message", res is None, repr(res))

    # 2. Blocked message (marker triggers fake 'Yes')
    res = await g.check_input("banned_word please")
    record("check_input blocks flagged message", res is not None and "can't respond" in res)

    # 3. Output rail allows a normal reply
    res = await g.check_output("Do your duty with a calm mind.")
    record("check_output allows safe reply", res is None)

    # 4. Output rail blocks flagged reply
    res = await g.check_output("banned_word reply")
    record("check_output blocks flagged reply", res is not None and "rather not share" in res)

    # 5. Disabled flag -> always allow
    g.GUARDRAILS_ENABLED = False
    res = await g.check_input("banned_word please")
    record("GUARDRAILS_ENABLED=false bypasses rails", res is None)
    g.GUARDRAILS_ENABLED = True

    # 6. Engine error -> fail-open (allow)
    class ExplodingRails:
        async def check_async(self, *a, **kw):
            raise RuntimeError("boom")

    saved = g._rails
    g._rails = ExplodingRails()
    res = await g.check_input("What is dharma?")
    record("rails engine crash -> fail-open (allow)", res is None)
    g._rails = saved

    # 7. Timeout -> fail-open (allow)
    import asyncio as aio

    class SlowRails:
        async def check_async(self, *a, **kw):
            await aio.sleep(30)

    g._rails = SlowRails()
    g.GUARDRAILS_TIMEOUT = 0.2
    res = await g.check_input("What is dharma?")
    record("rails timeout -> fail-open (allow)", res is None)
    g.GUARDRAILS_TIMEOUT = 10.0
    g._rails = saved


# ---------------------------------------------------------------------------
# Endpoint-level tests through FastAPI TestClient
# ---------------------------------------------------------------------------
async def endpoint_tests():
    print("\n=== ENDPOINT: /chat with rails active ===")

    # Fake the mentor-chain LLM so we test the whole endpoint without a key.
    # NOTE: must be a sync function — route_chain invokes the chain synchronously.
    from chains import mentor_chain
    from langchain_core.runnables.history import RunnableWithMessageHistory

    def fake_mentor_llm(prompt_value):
        return AIMessage(content="[fake mentor reply]")

    saved_chain, saved_memory = mentor_chain.base_chain, mentor_chain.chain_with_memory

    def make_chain(llm_fn):
        return RunnableWithMessageHistory(
            mentor_chain.prompt | llm_fn,
            mentor_chain.get_memory,
            input_messages_key="input",
            history_messages_key="history",
        )

    mentor_chain.base_chain = mentor_chain.prompt | fake_mentor_llm
    mentor_chain.chain_with_memory = make_chain(fake_mentor_llm)

    from fastapi.testclient import TestClient
    from app import app

    client = TestClient(app, raise_server_exceptions=False)

    rails_engine = build_fresh_rails()

    # -- input blocked --
    g._rails = rails_engine
    g._init_attempted = True
    client.post("/reset-memory/krishna")
    r = client.post("/chat", json={"mentor_id": "krishna", "user_message": "banned_word hello"})
    body = r.json()
    record("input rail blocks message -> canned refusal, 200",
           r.status_code == 200 and "can't respond" in body.get("reply", ""),
           f"status={r.status_code}, reply={body.get('reply', '')[:50]!r}")

    # -- input allowed -> mentor replies --
    r = client.post("/chat", json={"mentor_id": "krishna", "user_message": "What is my duty?"})
    body = r.json()
    record("safe message -> 200 with mentor reply",
           r.status_code == 200 and body.get("reply") == "[fake mentor reply]",
           f"status={r.status_code}")

    # -- output blocked --
    # Make the fake mentor LLM return a flagged reply, output rail should replace it
    def bad_mentor_llm(prompt_value):
        return AIMessage(content="banned_word secret advice")

    mentor_chain.base_chain = mentor_chain.prompt | bad_mentor_llm
    mentor_chain.chain_with_memory = make_chain(bad_mentor_llm)
    client.post("/reset-memory/krishna")
    r = client.post("/chat", json={"mentor_id": "krishna", "user_message": "What is my duty?"})
    body = r.json()
    record("output rail replaces unsafe reply -> safe replacement, 200",
           r.status_code == 200 and "rather not share" in body.get("reply", ""),
           f"reply={body.get('reply', '')[:60]!r}")

    # -- restore mentor chain --
    mentor_chain.base_chain, mentor_chain.chain_with_memory = saved_chain, saved_memory


# ---------------------------------------------------------------------------
async def main():
    await unit_tests()
    await endpoint_tests()

    print("\n=== SUMMARY ===")
    passed = sum(1 for _, ok in results if ok)
    print(f"{passed}/{len(results)} passed")
    if passed != len(results):
        for name, ok in results:
            if not ok:
                print(f"  FAILED: {name}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())

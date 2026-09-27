import logging

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from openai import (
    APIConnectionError,
    APITimeoutError,
    AuthenticationError,
    BadRequestError,
    InternalServerError,
    NotFoundError,
    PermissionDeniedError,
    RateLimitError,
)

from chains.chain_router import route_chain
from schemas.chat import ChatRequest, ChatResponse
from utils.mentor_loader import load_mentor
from utils.prompt_builder import build_system_prompt

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
logger = logging.getLogger("ai_mentor")

app = FastAPI(title="AI Mentor Backend")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # later restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def load_file(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def load_optional_file(path: str) -> str:
    """Load a prompt file, or return '' if it does not exist."""
    try:
        return load_file(path)
    except OSError:
        return ""


@app.get("/")
def root():
    return {"message": "AI Mentor backend running"}


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    try:
        mentor = load_mentor(req.mentor_id)
    except (OSError, ValueError) as e:
        logger.error("Mentor config could not be loaded: %s", e)
        raise HTTPException(
            status_code=500,
            detail="Mentor configuration is missing or invalid. Please contact the administrator.",
        )

    try:
        base_prompt = load_file("prompts/base.txt")
        safety_prompt = load_file("prompts/safety.txt")
        persona_prompt = load_optional_file(f"prompts/{mentor['id']}.txt")

        system_prompt = build_system_prompt(
            base_prompt,
            safety_prompt,
            persona_prompt,
            mentor,
        )

        reply = route_chain(system_prompt, req.user_message, mentor)

    except AuthenticationError:
        logger.error("LLM authentication failed — check OPENAI_API_KEY in backend/.env")
        raise HTTPException(
            status_code=502,
            detail="The AI service rejected its credentials. Please contact the administrator.",
        )
    except PermissionDeniedError:
        logger.error("LLM key lacks permission for the configured model")
        raise HTTPException(
            status_code=502,
            detail="The AI service denied access to the model. Please contact the administrator.",
        )
    except NotFoundError:
        logger.error("Configured LLM model was not found on the provider")
        raise HTTPException(
            status_code=502,
            detail="The AI model is currently unavailable. Please try again later.",
        )
    except RateLimitError:
        logger.warning("LLM rate limit reached")
        raise HTTPException(
            status_code=429,
            detail="The AI service is busy right now. Please try again in a few seconds.",
        )
    except APITimeoutError:
        logger.error("LLM request timed out")
        raise HTTPException(
            status_code=504,
            detail="The AI service took too long to respond. Please try again.",
        )
    except APIConnectionError:
        logger.error("Could not connect to the LLM provider")
        raise HTTPException(
            status_code=504,
            detail="The AI service is unreachable right now. Please try again shortly.",
        )
    except BadRequestError as e:
        logger.error("LLM rejected the request: %s", e)
        raise HTTPException(
            status_code=502,
            detail="The AI service could not process this request. Please rephrase and try again.",
        )
    except InternalServerError:
        logger.error("LLM provider internal error")
        raise HTTPException(
            status_code=502,
            detail="The AI service had an internal error. Please try again.",
        )
    except HTTPException:
        raise
    except Exception:
        logger.exception("Unhandled error in /chat")
        raise HTTPException(
            status_code=500,
            detail="Something went wrong on our side. Please try again.",
        )

    return {"reply": reply}


@app.post("/reset-memory/{mentor_id}")
def reset_memory(mentor_id: str):
    try:
        from chains.mentor_chain import MEMORY_STORE

        MEMORY_STORE.pop(mentor_id, None)
        return {"status": "memory cleared"}
    except Exception:
        logger.exception("Failed to reset memory for %s", mentor_id)
        raise HTTPException(
            status_code=500,
            detail="Could not clear chat memory. Please try again.",
        )

import os
from typing import Dict

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

from chains.rag_chain import build_rag_context

# Load environment variables
load_dotenv()

# ---------------- LLM ----------------
llm = ChatOpenAI(
    model=os.getenv("OPENAI_MODEL", "openai/gpt-3.5-turbo"),
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    openai_api_base=os.getenv("OPENAI_API_BASE"),
    temperature=0.7,
    default_headers={
        "HTTP-Referer": "http://localhost:5173",
        "X-Title": "AI Mentors App"
    }
)

# ---------------- MEMORY STORE ----------------
MEMORY_STORE: Dict[str, InMemoryChatMessageHistory] = {}

def get_memory(session_id: str) -> InMemoryChatMessageHistory:
    if session_id not in MEMORY_STORE:
        MEMORY_STORE[session_id] = InMemoryChatMessageHistory()
    return MEMORY_STORE[session_id]

# ---------------- PROMPT (CRITICAL FIX) ----------------
prompt = ChatPromptTemplate.from_messages([
    ("system", "{system_prompt}"),
    ("placeholder", "{history}"),   # ← MEMORY IS INJECTED HERE
    ("human", "{input}")
])

# ---------------- CHAIN ----------------
base_chain = prompt | llm

chain_with_memory = RunnableWithMessageHistory(
    base_chain,
    get_memory,
    input_messages_key="input",
    history_messages_key="history",
)

# ---------------- PUBLIC FUNCTION ----------------
def run_mentor_chain(
    system_prompt: str,
    user_message: str,
    mentor_id: str,
    retriever=None,
) -> str:
    """
    mentor_id should uniquely represent:
    - user + mentor (example: user123_rama)

    If a retriever is provided, retrieved context is added to the
    human turn (memory still applies to the same session).
    """
    if retriever is not None:
        context = build_rag_context(retriever, user_message)

        if context:
            augmented = (
                f"{user_message}\n\n"
                f"(Relevant passages from my teachings, use if helpful:\n{context})"
            )
            user_message = augmented

    response = chain_with_memory.invoke(
        {
            "input": user_message,
            "system_prompt": system_prompt,
        },
        config={
            "configurable": {
                "session_id": mentor_id
            }
        }
    )
    return response.content

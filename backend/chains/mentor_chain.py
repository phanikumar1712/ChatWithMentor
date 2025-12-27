 
import os
from dotenv import load_dotenv
from typing import Dict

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

load_dotenv()

# LLM (unchanged logic)
llm = ChatOpenAI(
    model=os.getenv("OPENAI_MODEL", "openai/gpt-3.5-turbo"),
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    openai_api_base=os.getenv("OPENAI_API_BASE"),
    default_headers={
        "HTTP-Referer": "http://localhost:5173",
        "X-Title": "AI Mentors App"
    },
    temperature=0.7
)

# ---- MEMORY STORE (same idea as before) ----
MEMORY_STORE: Dict[str, InMemoryChatMessageHistory] = {}

def get_memory(mentor_id: str) -> InMemoryChatMessageHistory:
    if mentor_id not in MEMORY_STORE:
        MEMORY_STORE[mentor_id] = InMemoryChatMessageHistory()
    return MEMORY_STORE[mentor_id]

# ---- PROMPT (same structure) ----
prompt = ChatPromptTemplate.from_messages([
    ("system", "{system_prompt}"),
    ("human", "{input}")
])

# ---- CHAIN ----
base_chain = prompt | llm

chain_with_memory = RunnableWithMessageHistory(
    base_chain,
    get_memory,
    input_messages_key="input",
    history_messages_key="history",
)

# ---- PUBLIC FUNCTION (same signature & behavior) ----
def run_mentor_chain(system_prompt: str, user_message: str, mentor_id: str) -> str:
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


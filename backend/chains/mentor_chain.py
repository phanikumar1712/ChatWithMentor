 
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

 
 
# import os
# from dotenv import load_dotenv
# from typing import Dict

# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain_core.prompts import ChatPromptTemplate
# from langchain_core.chat_history import InMemoryChatMessageHistory
# from langchain_core.runnables.history import RunnableWithMessageHistory

# load_dotenv()  # Loads GOOGLE_API_KEY from .env

# # LLM - Google Gemini (free tier optimized)
# llm = ChatGoogleGenerativeAI(
#     model=os.getenv("GEMINI_MODEL", "gemini-2.5-flash-lite"),  # Lightest model = max free quota (~20-25/day)
#     temperature=0.7,
#     convert_system_message_to_human=True,  # Critical: lets Gemini properly handle system prompts
# )

# # ---- MEMORY STORE (per mentor/session) ----
# MEMORY_STORE: Dict[str, InMemoryChatMessageHistory] = {}

# def get_memory(mentor_id: str) -> InMemoryChatMessageHistory:
#     if mentor_id not in MEMORY_STORE:
#         MEMORY_STORE[mentor_id] = InMemoryChatMessageHistory()
#     return MEMORY_STORE[mentor_id]

# # ---- PROMPT (must include history placeholder for memory to work) ----
# prompt = ChatPromptTemplate.from_messages([
#     ("system", "{system_prompt}"),
#     ("placeholder", "{history}"),   # This inserts past messages
#     ("human", "{input}")
# ])

# # ---- CHAIN ----
# base_chain = prompt | llm

# # Add conversation memory (one history per mentor_id)
# chain_with_memory = RunnableWithMessageHistory(
#     base_chain,
#     get_memory,
#     input_messages_key="input",
#     history_messages_key="history",  # Matches the placeholder above
# )

# # ---- PUBLIC FUNCTION (exact same signature & behavior as OpenAI version) ----
# def run_mentor_chain(system_prompt: str, user_message: str, mentor_id: str) -> str:
#     """
#     Run Gemini mentor conversation with persistent memory per mentor_id.
    
#     Args:
#         system_prompt: Role and instructions for the mentor
#         user_message: User's latest message
#         mentor_id: Unique session identifier (e.g., "math_tutor_123")
    
#     Returns:
#         Gemini's response string
#     """
#     response = chain_with_memory.invoke(
#         {
#             "input": user_message,
#             "system_prompt": system_prompt,
#         },
#         config={"configurable": {"session_id": mentor_id}}
#     )
#     return response.content
# import os
# from dotenv import load_dotenv
# from langchain.chat_models import ChatOpenAI
# from langchain.prompts import ChatPromptTemplate

# load_dotenv()

# llm = ChatOpenAI(
#     model_name="openai/gpt-3.5-turbo",
#     openai_api_key=os.getenv("OPENAI_API_KEY"),
#     openai_api_base="https://openrouter.ai/api/v1",
#     default_headers={
#         "HTTP-Referer": "http://localhost:3000",
#         "X-Title": "AI Mentor Project"
#     }
# )

# def run_mentor_chain(system_prompt: str, user_message: str) -> str:
#     prompt = ChatPromptTemplate.from_messages([
#         ("system", system_prompt),
#         ("human", user_message)
#     ])

#     chain = prompt | llm
#     response = chain.invoke({})

#     return response.content

import os
from dotenv import load_dotenv
# from langchain.chat_models import ChatOpenAI
from langchain_community.chat_models import ChatOpenAI

from langchain.prompts import ChatPromptTemplate
from langchain.memory import ConversationBufferMemory

load_dotenv()

llm = ChatOpenAI(
    model_name="openai/gpt-3.5-turbo",
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    openai_api_base="https://openrouter.ai/api/v1",
    default_headers={
        "HTTP-Referer": "http://localhost:5173",
        "X-Title": "AI Mentor App"
    }
)

MEMORY_STORE = {}

def get_memory(mentor_id):
    if mentor_id not in MEMORY_STORE:
        MEMORY_STORE[mentor_id] = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
    return MEMORY_STORE[mentor_id]


def run_mentor_chain(system_prompt, user_message, mentor_id):
    memory = get_memory(mentor_id)

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("placeholder", "{chat_history}"),
        ("human", "{input}")
    ])

    chain = prompt | llm

    response = chain.invoke({
        "input": user_message,
        "chat_history": memory.load_memory_variables({})["chat_history"]
    })

    memory.save_context(
        {"input": user_message},
        {"output": response.content}
    )

    return response.content

from chains.mentor_chain import run_mentor_chain
from utils.retriever_factory import get_retriever

def route_chain(system_prompt: str, user_message: str, mentor: dict) -> str:
    retriever = None
    if mentor.get("rag_enabled", False):
        retriever = get_retriever(mentor["id"])

    return run_mentor_chain(
        system_prompt=system_prompt,
        user_message=user_message,
        mentor_id=mentor["id"],
        retriever=retriever,
    )

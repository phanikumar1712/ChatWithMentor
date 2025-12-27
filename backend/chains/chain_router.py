# from chains.mentor_chain import run_mentor_chain

# def route_chain(system_prompt, user_message, mentor):
#     # RAG can be added later here
#     return run_mentor_chain(system_prompt, user_message)




from chains.mentor_chain import run_mentor_chain


def route_chain(system_prompt: str, user_message: str, mentor: dict) -> str:
    return run_mentor_chain(
        system_prompt=system_prompt,
        user_message=user_message,
        mentor_id=mentor["id"]
    )

import os
from fastapi import FastAPI
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

from schemas.chat import ChatRequest, ChatResponse
from utils.mentor_loader import load_mentor
from utils.prompt_builder import build_system_prompt
from chains.chain_router import route_chain

load_dotenv()

app = FastAPI(title="AI Mentor Backend")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # later restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
def load_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()
        
@app.get("/")
def root():
    return {"message": "AI Mentor backend running"} 


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    mentor = load_mentor(req.mentor_id)

    base_prompt = load_file("prompts/base.txt")
    safety_prompt = load_file("prompts/safety.txt")
    persona_prompt = load_file(f"prompts/{mentor['id']}.txt")

    system_prompt = build_system_prompt(
        base_prompt,
        safety_prompt,
        persona_prompt,
        mentor
    )

    reply = route_chain(
        system_prompt,
        req.user_message,
        mentor
    )

    return {"reply": reply}



@app.post("/reset-memory/{mentor_id}")
def reset_memory(mentor_id: str):
    from chains.mentor_chain import MEMORY_STORE
    MEMORY_STORE.pop(mentor_id, None)
    return {"status": "memory cleared"}



# import os
# from fastapi import FastAPI
# from dotenv import load_dotenv
# from fastapi.middleware.cors import CORSMiddleware

# from schemas.chat import ChatRequest, ChatResponse
# from utils.mentor_loader import load_mentor
# from utils.prompt_builder import build_system_prompt
# from chains.chain_router import route_chain

# load_dotenv()

# app = FastAPI(title="AI Mentor Backend")
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # later restrict in production
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )
# def load_file(path):
#     with open(path, "r", encoding="utf-8") as f:
#         return f.read()
        
# @app.get("/")
# def root():
#     return {"message": "AI Mentor backend running"} 


# @app.post("/chat", response_model=ChatResponse)
# def chat(req: ChatRequest):
#     mentor = load_mentor(req.mentor_id)

#     base_prompt = load_file("prompts/base.txt")
#     safety_prompt = load_file("prompts/safety.txt")
#     persona_prompt = load_file(f"prompts/{mentor['id']}.txt")

#     system_prompt = build_system_prompt(
#         base_prompt,
#         safety_prompt,
#         persona_prompt,
#         mentor
#     )

#     reply = route_chain(
#         system_prompt,
#         req.user_message,
#         mentor
#     )

#     return {"reply": reply}



# @app.post("/reset-memory/{mentor_id}")
# def reset_memory(mentor_id: str):
#     from chains.mentor_chain import MEMORY_STORE
#     MEMORY_STORE.pop(mentor_id, None)
#     return {"status": "memory cleared"}

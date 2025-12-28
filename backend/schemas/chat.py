from pydantic import BaseModel

class ChatRequest(BaseModel):
    mentor_id: str
    user_message: str

class ChatResponse(BaseModel):
    reply: str


# from pydantic import BaseModel

# class ChatRequest(BaseModel):
#     mentor_id: str
#     user_message: str

# class ChatResponse(BaseModel):
#     reply: str

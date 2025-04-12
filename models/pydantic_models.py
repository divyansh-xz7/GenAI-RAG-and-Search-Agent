from pydantic import BaseModel
from typing import List


# contains pydantic models for response and requests

class UserBase(BaseModel):
    name : str

class ChatSessionBase(BaseModel):
    user_id: int

class ChatHistoryBase(BaseModel):
    session_id: int
    chat : str

class User(UserBase):
    user_id: int
    sessions: List[ChatSessionBase] = []
    class Config:
        orm_mode = True

class ChatSession(ChatSessionBase):
    session_id: int
    summary: str
    class Config:
        orm_mode = True

class ChatHistory(ChatHistoryBase):
    chat_id: int
    class Config:
        orm_mode = True
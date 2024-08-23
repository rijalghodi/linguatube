from typing import List, Literal, Optional, TypedDict

from pydantic import BaseModel


class Message(TypedDict):
    id: str
    video_id: str
    message: Optional[str]
    created_at: str


class InsertMessageRequest(BaseModel):
    role: str
    content: str
    api_key: str

class MessageData(BaseModel):
    role: str
    content: str

class MessageListData(BaseModel):
    data: List[MessageData]
    count: int

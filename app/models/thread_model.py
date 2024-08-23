from typing import List, Literal, Optional, TypedDict

from pydantic import BaseModel


class Thread(TypedDict):
    id: str
    video_id: str
    thread_id: str
    created_at: str
    
class ThreadData(BaseModel):
    pass

class ThreadMetaData(BaseModel):
    id: str
    video_id: str
    thread_id: str
    created_at: str
    title: Optional[str]
    mode: Optional[str]
    
class ThreadListData(BaseModel):
    data: List[ThreadMetaData]
    count: int

class CreateThreadRequest(BaseModel):
    title: Optional[str]
    mode: Optional[Literal["chat", "practice"]] = "chat"
    api_key: str


from typing import Optional, TypedDict

from pydantic import BaseModel


class Video(TypedDict):
    id: str
    title: Optional[str]
    description: Optional[str]
    author: Optional[str]
    youtube_id: str
    created_at: str

class CreateVideoRequest(BaseModel):
    youtube_id: str
    title: Optional[str]
    description: Optional[str]
    author: Optional[str]

class VideoData(BaseModel):
    id: str
    title: Optional[str]
    description: Optional[str]
    author: Optional[str]
    youtube_id: str
    created_at: str
    
    
class ListVideoData(BaseModel):
    data: list[VideoData]
    count: Optional[int]
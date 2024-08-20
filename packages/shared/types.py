from typing import TypedDict, Optional

class Video(TypedDict):
    id: str
    title: Optional[str]
    description: Optional[str]
    author: Optional[str]
    youtube_id: str
    created_at: str

class Transcript(TypedDict):
    id: str
    video_id: str
    transcript: str
    plain_transcript: Optional[str]
    created_at: str

class Message(TypedDict):
    id: str
    video_id: str
    message: Optional[str]
    created_at: str
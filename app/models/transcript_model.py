from typing import Optional, TypedDict

from pydantic import BaseModel


class Transcript(TypedDict):
    id: str
    video_id: str
    transcript: str
    plain_transcript: Optional[str]
    created_at: str

class CreateTranscriptRequest(BaseModel):
    transcript_list: str
    plain_transcript: Optional[str]

class TranscriptData(BaseModel):
    id: str
    video_id: str
    transcript: str
    plain_transcript: Optional[str]
    created_at: str

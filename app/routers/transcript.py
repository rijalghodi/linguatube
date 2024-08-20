from pydantic import BaseModel
from fastapi import APIRouter, Depends
from supabase import Client
from typing import Optional

from packages import find_video_by_id, find_transcript_by_video_id
from packages.shared import SupabaseClient

from packages.service import insert_transcript


class CreateTranscriptRequest(BaseModel):
    transcript_list: str
    plain_transcript: Optional[str]

class TranscriptData(BaseModel):
    id: str
    video_id: str
    transcript: str
    plain_transcript: Optional[str]
    created_at: str


router = APIRouter()

def get_client():
    return SupabaseClient()

@router.post("/video/{video_id}/transcript/", response_model=TranscriptData)
def create_transcript(video_id: str, req: CreateTranscriptRequest, client: Client = Depends(get_client) ):
    transcript = insert_transcript(client, req["transcript_list"], video_id, plain_transcript=req["plain_transcript"])
    return transcript

@router.get("/video/{video_id}/transcript/", response_model=TranscriptData)
def get_transcript_by_video_id(video_id: str, client: Client = Depends(get_client) ):
    transcript = find_transcript_by_video_id(client, video_id)
    return transcript


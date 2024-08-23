from fastapi import APIRouter, Depends, HTTPException
from supabase import Client

from app.core.db_client import get_client
from app.models import CreateTranscriptRequest, TranscriptData
from app.service import find_transcript_by_video_id, insert_transcript

router = APIRouter()

@router.post("/video/{video_id}/transcript/", response_model=TranscriptData)
async def create_transcript(video_id: str, req: CreateTranscriptRequest, client: Client = Depends(get_client)) -> TranscriptData:
    try:
        transcript = insert_transcript(client, req["transcript_list"], video_id, plain_transcript=req["plain_transcript"])
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while creating transcript." + str(e))
    return transcript

@router.get("/video/{video_id}/transcript/", response_model=TranscriptData)
async def get_transcript_by_video_id(video_id: str, client: Client = Depends(get_client)) -> TranscriptData:
    try:
        transcript = find_transcript_by_video_id(client, video_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while fetching transcript." + str(e))
    return transcript


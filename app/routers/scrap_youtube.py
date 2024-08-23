import json

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from supabase import Client

from app.core.db_client import get_client
from app.models import TranscriptData, VideoData
from app.routers.transcript import create_transcript
from app.routers.video import create_video
from app.utils import scrap_youtube_metadata, scrap_youtube_transcript


class ScrapYoutubeRequest(BaseModel):
    youtube_id: str

class ScrapYoutubeData(BaseModel):
    video: VideoData
    transcript: TranscriptData

router = APIRouter()

@router.post("/scrap-youtube/", response_model=ScrapYoutubeData)
def scrap_youtube(req: ScrapYoutubeRequest, client: Client = Depends(get_client)):
    # Create video
    youtube_id = req.youtube_id
    metadata = scrap_youtube_metadata(youtube_id)
    new_video_data = {
        "title": metadata["title"],
        "description": metadata["description"],
        "author": metadata["author"],
        "youtube_id": youtube_id,
    }
    video = create_video(new_video_data, client=client)
    
    # Create transcript
    try:
        transcript_list, plain_transcript = scrap_youtube_transcript(youtube_id)
    except Exception as e:
        print("An error occurred while fetching the transcript. This video might not have a transcript available.")
        raise HTTPException(
            status_code=500,
            detail="An error occurred while fetching the transcript. This video might not have a transcript available." + str(e)
        )

    new_transcript_data = {
        "transcript_list" : json.dumps(transcript_list),
        "plain_transcript" : plain_transcript,
    }
    
    try:
        transcript = create_transcript(video['id'], new_transcript_data, client=client)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    return {
        "video": video,
        "transcript": transcript,
    }



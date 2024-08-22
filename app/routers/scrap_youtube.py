import json

from pydantic import BaseModel
from fastapi import APIRouter, Depends
from supabase import Client
from packages.shared import supabase_client

from app.routers.video import create_video, VideoData
from app.routers.transcript import create_transcript, TranscriptData
from packages.utils import scrap_youtube_transcript, scrap_youtube_metadata
from app.core.db_client import get_client


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
    transcript_list, plain_transcript = scrap_youtube_transcript(youtube_id)
    new_transcript_data = {
        "transcript_list" : json.dumps(transcript_list),
        "plain_transcript" : plain_transcript,
    }
    transcript = create_transcript(video['id'], new_transcript_data, client=client)

    return {
        "video": video,
        "transcript": transcript,
    }



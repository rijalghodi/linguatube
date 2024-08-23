from fastapi import APIRouter, Depends, HTTPException
from supabase import Client

from app.core.db_client import get_client
from app.models import CreateVideoRequest, VideoData
from app.service import find_video_by_id, insert_video

router = APIRouter()

@router.post("/video/", response_model=VideoData)
def create_video(req: CreateVideoRequest, client: Client = Depends(get_client)):
    try:
        video = insert_video(
            client,
            req["youtube_id"],
            title=req["title"],
            description=req["description"],
            author=req["author"],
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while creating video." + str(e))

    return video

@router.get("/video/{video_id}", response_model=VideoData)
def get_video(video_id: str, client: Client = Depends(get_client) ):
    try:
        video = find_video_by_id(client, video_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while fetching video." + str(e))
    return video


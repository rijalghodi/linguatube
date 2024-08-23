from fastapi import APIRouter, Depends, HTTPException
from supabase import Client

from app.core.db_client import get_client
from app.models import CreateVideoRequest, ListVideoData, VideoData
from app.service import find_all_video, find_video_by_id, insert_video

router = APIRouter()

@router.post("/video/", response_model=ListVideoData)
async def create_video(req: CreateVideoRequest, client = (get_client)) -> VideoData:
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
async def get_video(video_id: str, client: Client = Depends(get_client)) -> VideoData:
    try:
        video = find_video_by_id(client, video_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while fetching video." + str(e))
    return video

@router.get("/video/", response_model=ListVideoData)
async def get_video(count: int, client: Client = Depends(get_client)) -> ListVideoData:
    try:
        video = find_all_video(client, count)
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while fetching all video." + str(e))
    return {
        "count": len(video),
        "data": video
    }


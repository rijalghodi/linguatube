from pydantic import BaseModel
from fastapi import APIRouter, Depends
from supabase import Client
from typing import Optional

from packages import find_video_by_id
from app.core.db_client import get_client

from packages.service import insert_video


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

router = APIRouter()

@router.post("/video/", response_model=VideoData)
def create_video(req: CreateVideoRequest, client: Client = Depends(get_client) ):
    # Create video
    video = insert_video(
        client,
        req["youtube_id"],
        title=req["title"],
        description=req["description"],
        author=req["author"],
    )

    return video

@router.get("/video/{video_id}", response_model=VideoData)
def get_video(video_id: str, client: Client = Depends(get_client) ):
    video = find_video_by_id(client, video_id)
    return video


import uuid
from typing import Optional

from supabase import Client

from app.models import Video


def insert_video(
    client: Client,
    youtube_id: str, 
    author: Optional[str] = None, 
    title: Optional[str] = None, 
    description: Optional[str] = None
) -> Video:
    random_uuid = str(uuid.uuid4())
    video_data = {
        "id": random_uuid,
        "youtube_id": youtube_id,
        "author": author,
        "title": title,
        "description": description,
    }
    response = (
        client.table("video")
        .insert(video_data)
        .execute()
    ).model_dump()

    return response["data"][0]

from pydantic import BaseModel
from fastapi import APIRouter, Depends
from supabase import Client

from app.routers.transcript import get_transcript_by_video_id
from app.routers.video import get_video
from packages import split_text, texts_to_docs
from app.core.db_client import get_client

from packages.service import insert_document

class DocumentData(BaseModel):
    ids: list[str]
router = APIRouter()

@router.post("/video/{video_id}/document/", response_model=DocumentData)
def create_document(video_id: str, client: Client = Depends(get_client)):
    transcript = get_transcript_by_video_id(video_id, client)
    metadata = get_video(video_id, client)
    texts = split_text(transcript["plain_transcript"])
    documents = texts_to_docs(texts, {
        "video_id": video_id,
        "title": metadata["title"],
        "description": metadata["description"],
        "author": metadata["author"],
        "youtube_id": metadata["youtube_id"]
    })
    response = insert_document(client, documents)
    return {"ids": response}

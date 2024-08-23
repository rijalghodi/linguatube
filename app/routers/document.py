from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from supabase import Client

from app.core.db_client import get_client
from app.core.vectorstore import get_vectorstore
from app.routers.transcript import get_transcript_by_video_id
from app.routers.video import get_video
from app.service import insert_document
from app.utils import split_text, texts_to_docs


class DocumentData(BaseModel):
    ids: list[str]

class DocumentRequest(BaseModel):
    api_key: str
router = APIRouter()

@router.post("/video/{video_id}/document/", response_model=DocumentData)
async def create_document( request: DocumentRequest, video_id: str, client: Client = Depends(get_client)):
    try:
        transcript = await get_transcript_by_video_id(video_id, client)
        
        if not transcript:
            raise HTTPException(status_code=404, detail="Transcript not found.")
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while fetching transcript." + str(e))
    
    try:
        metadata = await get_video(video_id, client)
        
        if not metadata:
            raise HTTPException(status_code=404, detail="Video metadata not found.")
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while fetching video metadata." + str(e))

    print(metadata)
    texts = split_text(transcript["plain_transcript"])
    documents = texts_to_docs(texts, {
        "video_id": video_id,
        "title": metadata.get("title", ""),
        "description": metadata.get("description", ""),
        "author": metadata.get("author", ""),
        "youtube_id": metadata.get("youtube_id", "")
    })
    
    try:
        response = insert_document(client, documents, request.api_key)
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while inserting documents. " + str(e))
        
    return {"ids": response}

class GetAllDocumentData(BaseModel):
    count: int

@router.get("/video/{video_id}/document/", response_model=GetAllDocumentData)
async def get_all_document(video_id: str, api_key: str, client: Client = Depends(get_client)):
    
    vector_store = get_vectorstore(api_key, client)
    try:
        res = vector_store.similarity_search("Anything", k=4, filter={"video_id": video_id})
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while getting documents. "+str(e))

    return {"count": len(res)}

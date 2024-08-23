import uuid
from typing import Optional

from supabase import Client

from app.models import Transcript


def insert_transcript(
    client: Client,
    transcript_list: str, # JSON Stringify
    video_id: str,
    plain_transcript: Optional[str] = None
) -> Transcript:
    random_uuid = str(uuid.uuid4())
    transcript_data = {
        "id": random_uuid,
        "video_id": video_id,
        "transcript": transcript_list,
        "plain_transcript": plain_transcript,
    }
    response = (
        client.table("transcript")
        .insert(transcript_data)
        .execute()
    ).model_dump()

    return response["data"][0]

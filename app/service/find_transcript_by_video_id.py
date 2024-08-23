from supabase import AClient

from app.models import Transcript


def find_transcript_by_video_id(
    client: AClient,
    video_id: str,
) -> Transcript:
    response =  client \
        .table("transcript") \
        .select("*") \
        .eq("video_id", video_id) \
        .single().execute().model_dump()

    return response["data"]
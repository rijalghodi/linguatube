from packages.shared import Transcript
from supabase import Client

def find_transcript_by_video_id(
    client: Client,
    video_id: str,
) -> Transcript:
    response = client \
        .from_("transcript") \
        .select("*") \
        .eq("video_id", video_id) \
        .single().execute().model_dump()

    return response["data"]
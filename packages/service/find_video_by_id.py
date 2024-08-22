from packages.shared import Video
from supabase import Client

def find_video_by_id(
    client: Client,
    id: str,
) -> Video:
    response = client \
        .from_("video") \
        .select("*") \
        .eq("id", id) \
        .single().execute().model_dump()

    return response["data"]

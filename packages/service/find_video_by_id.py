from packages.shared import SupabaseClient, Video
from supabase import Client

def find_video_by_id(
    client: Client,
    id: str,
) -> Video:
    sc = SupabaseClient()
    response = client \
        .from_("video") \
        .select("*") \
        .eq("id", id) \
        .single().execute().model_dump()

    return response["data"]

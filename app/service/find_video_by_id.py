from supabase import Client

from app.models import Video


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

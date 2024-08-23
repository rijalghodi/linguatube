from supabase import Client

from app.models import Video


def find_all_video(
    client: Client,
    count: int = 5,
) -> Video:
    response =  client \
        .from_("video") \
        .select("*").order('created_at', desc=True) \
        .limit(count).execute().model_dump()
    return response["data"]

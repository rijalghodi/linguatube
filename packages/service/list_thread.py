from packages.shared import Video
from supabase import Client

def list_thread(
    client: Client,
    video_id: str = None,
) -> Video:
    query = client \
        .table("checkpoint_metadata") \
        .select("*", count='exact')

    if video_id:
        query = query.eq("video_id", video_id)

    response = query.execute()

    return response

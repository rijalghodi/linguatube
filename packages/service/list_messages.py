

from packages.shared import Video
from supabase import Client

def list_message(
    client: Client,
    thread_id: str,
    graph: str = None,
) -> Video:

    query = client \
        .table("checkpoint_metadata") \
        .select("*", count='exact')

    if graph:
        query = query.eq("video_id", video_id)

    response = query.execute()

    return response

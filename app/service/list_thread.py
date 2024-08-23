from supabase import Client

from app.models import Thread


def list_thread(
    client: Client,
    video_id: str = None,
) -> Thread:
    query = client \
        .table("checkpoint_metadata") \
        .select("*", count='exact')

    if video_id:
        query = query.eq("video_id", video_id)

    response = query.execute()

    return response

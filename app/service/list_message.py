from supabase import Client

from app.models import Video


def list_message(
    client: Client,
    thread_id: str,
    graph: str = None,
) -> Video:

    query = client \
        .table("checkpoint_metadata") \
        .select("*", count='exact')

    if graph:
        query = query.eq("thread_id", thread_id)

    response = query.execute()

    return response

from typing import Literal

from supabase import Client

from app.models import ThreadMetaData


def insert_thread(
    client: Client,
    video_id: str, # JSON Stringify
    thread_id: str,
    title: str = "",
    mode: Literal["chat", "practice"] = "chat",
) -> ThreadMetaData:
    data = {
        "video_id": video_id,
        "thread_id": thread_id,
        "title": title,
        "mode": mode
    }
    response = (
        client.table("checkpoint_metadata")
        .insert(data)
        .execute()
    ).model_dump()

    return response["data"][0]

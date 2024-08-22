from packages.shared import Transcript
from packages.shared.types import ThreadMetadata
from supabase import Client
from typing import Literal

def insert_thread(
    client: Client,
    video_id: str, # JSON Stringify
    thread_id: str,
    title: str = "",
    mode: Literal["chat", "practice"] = "chat",
) -> ThreadMetadata:
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

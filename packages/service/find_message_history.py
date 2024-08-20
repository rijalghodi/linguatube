from packages.shared import SupabaseClient
from typing import List, Tuple
from supabase import Client

from packages import deserialize_message_from_str


def find_message_history(
    client: Client,
    video_id: str,
) -> List[Tuple[str, str]]:
    sc = SupabaseClient()
    data = client \
        .from_("message") \
        .select("*") \
        .eq("video_id", video_id) \
        .execute().model_dump()["data"]
    messages = [deserialize_message_from_str(message["message"]) for message in data]

    return messages
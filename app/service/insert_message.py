import uuid

from supabase import Client

from app.models import Message


def insert_message(
    client: Client,
    message: str,
    video_id: str,
) -> Message:
    random_uuid = str(uuid.uuid4())
    message_data = {
        "id": random_uuid,
        "video_id": video_id,
        "message": message,
    }
    response = (
        client.table("message")
        .insert(message_data)
        .execute()
    ).model_dump()

    return response["data"][0]

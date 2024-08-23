from packages import SupabaseClient, find_video_by_id
import os
from dotenv import load_dotenv

if __name__ == '__main__':
    load_dotenv()

    client = SupabaseClient()
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")

    messages = find_video_by_id(client, "1fbf5008-05cd-4bc1-a0ec-201d787d093d")

    # result = [deserialize_message_from_str(message["message"]) for message in messages]

    print(messages)
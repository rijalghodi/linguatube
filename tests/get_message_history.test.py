from app.service import find_message_history
import os
from dotenv import load_dotenv

if __name__ == '__main__':
    load_dotenv()

    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")

    messages = find_message_history("247e3ca7-e281-4012-a6cc-7208e3fcb223")

    # result = [deserialize_message_from_str(message["message"]) for message in messages]

    print(messages)
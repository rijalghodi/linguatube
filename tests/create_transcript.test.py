from app.service import insert_transcript
import json
import os
from dotenv import load_dotenv

if __name__ == '__main__':
    load_dotenv()

    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")

    transcript_dict = [
        {
            "timestamp": "00.00.00",
            "text": "Hello"
        }
    ]

    transcript_string = json.dumps(transcript_dict)

    res = insert_transcript(transcript_string, video_id="247e3ca7-e281-4012-a6cc-7208e3fcb223", plain_transcript="")
    print(res)
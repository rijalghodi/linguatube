from packages.service import insert_video
import os
from dotenv import load_dotenv

if __name__ == '__main__':

    load_dotenv()

    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")

    res = insert_video("Hello 123", author="A", title="Title", description="Description")
    print(res)

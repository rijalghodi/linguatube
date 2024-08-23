import os

from dotenv import load_dotenv
from supabase import Client, create_client

load_dotenv()

db_url = os.getenv("SUPABASE_URL")
db_key = os.getenv("SUPABASE_KEY")

def get_client() -> Client:
    return create_client(db_url, db_key)

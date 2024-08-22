from dotenv import load_dotenv
import os
from supabase import create_client, Client

load_dotenv()

db_url = os.getenv("SUPABASE_URL")
db_key = os.getenv("SUPABASE_KEY")

def get_client() -> Client:
    return create_client(db_url, db_key)

from supabase import create_client, Client
import os

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
def get_supabase_client():
    return create_client(url, key)

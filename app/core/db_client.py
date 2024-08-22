from dotenv import load_dotenv
import os
from psycopg_pool import ConnectionPool
from psycopg.rows import dict_row
from supabase import create_client, Client

load_dotenv()

db_url = os.getenv("SUPABASE_URL")
db_key = os.getenv("SUPABASE_KEY")

def get_client() -> Client:
    return create_client(db_url, db_key)

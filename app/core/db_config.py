from dotenv import load_dotenv
import os
from psycopg_pool import ConnectionPool
from psycopg.rows import dict_row
from supabase import create_client, Client

load_dotenv()

connection_kwargs ={
    "autocommit": True,
    "prepare_threshold": 0,
    "row_factory": dict_row,
}

db_pool_uri = os.getenv("SUPABASE_CONNECTION_URI")
def create_supabase_pool() -> ConnectionPool:
    return ConnectionPool(
        conninfo=db_pool_uri,
        max_size=20,
        kwargs=connection_kwargs
    )

db_url = os.getenv("SUPABASE_URL")
db_key = os.getenv("SUPABASE_KEY")
def create_supabase_client() -> Client:
    return create_client(db_url, db_key)

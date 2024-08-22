from dotenv import load_dotenv
import os
from psycopg_pool import ConnectionPool
from psycopg.rows import dict_row

load_dotenv()

connection_kwargs ={
    "autocommit": True,
    "prepare_threshold": 0,
    "row_factory": dict_row,
}

def get_supabase_pool():
    return ConnectionPool(
        conninfo=os.getenv("SUPABASE_CONNECTION_URI"),
        max_size=20,
        kwargs=connection_kwargs
    )
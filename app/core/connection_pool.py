import os

from dotenv import load_dotenv
from psycopg.rows import dict_row
from psycopg_pool import ConnectionPool

load_dotenv()

connection_kwargs ={
    "autocommit": True,
    "prepare_threshold": 0,
    "row_factory": dict_row,
}

db_pool_uri = os.getenv("SUPABASE_CONNECTION_URI")
def get_connection_pool() -> ConnectionPool:
    return ConnectionPool(
        conninfo=db_pool_uri,
        max_size=10,
        kwargs=connection_kwargs
    )


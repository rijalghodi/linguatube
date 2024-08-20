from supabase import create_client, Client
import os

class SupabaseClient:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            # Initialize the Supabase client only once
            url = os.getenv("SUPABASE_URL")
            key = os.getenv("SUPABASE_KEY")
            cls._instance = create_client(url, key)
        return cls._instance

# Usage example
if __name__ == "__main__":
    client = SupabaseClient()
    print(client)

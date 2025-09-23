import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables
load_dotenv()
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")

def get_supabase_client() -> Client:
    """
    Initializes and returns a Supabase client.
    """
    if not url or not key:
        raise ValueError("Supabase URL and Key must be set in the .env file.")
    try:
        return create_client(url, key)
    except Exception as e:
        raise ConnectionError(f"Error creating Supabase client: {e}")

supabase = get_supabase_client()
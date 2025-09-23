import random
from supabase_client import supabase
from typing import Optional  # <-- Add this import

def get_song_recommender(mood: str) -> Optional[dict]:
    """
    Fetches a random song from the Supabase database based on the detected mood.
    :param mood: The mood to filter songs by.
    :return: A dictionary containing song details or None if no songs are found.
    """
    try:
        response = supabase.table('newsongs').select('*').eq('mood', mood).execute()
        
        if response.data and len(response.data) > 0:
            return random.choice(response.data)
        else:
            return None
    except Exception as e:
        print(f"An error occurred while fetching a song: {e}")
        return None
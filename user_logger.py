# user_logger.py

from supabase_client import supabase
import streamlit as st 

def log_user_interaction(user_id: int, user_input: str, detected_mood: str, recommended_song_id: int):
    """
    Logs a user's interaction and song recommendation to the database.
    (Omitted for brevity, assume function body is correct)
    """
    try:
        data_to_log = {
            "user_id": user_id,
            "song_id": recommended_song_id,
            "user_input": user_input,
            "detected_mood": detected_mood
        }
        response = supabase.table("user_recommendations").insert(data_to_log).execute()
        if response.data:
            st.toast("Interaction logged successfully.", icon="💾")
    except Exception as e:
        st.caption(f"Error logging interaction: {e}")


def get_user_history(user_id):
    """
    Fetches the last 5 recommendations for the given user ID, joining with the newsongs table.
    """
    try:
        # FIX: Changed 'songs' to 'newsongs' in the select statement
        response = supabase.table('user_recommendations').select(
            'timestamp, user_input, detected_mood, newsongs(song_title, artists, link)' 
        ).eq('user_id', user_id).order('timestamp', desc=True).limit(5).execute()
        
        if response.data:
            history = []
            for item in response.data:
                timestamp_str = item['timestamp'].split('.')[0].replace('T', ' ')
                # FIX: Use 'newsongs' key for data retrieval
                song_data = item['newsongs'] if item.get('newsongs') else {'song_title': 'N/A', 'artists': 'N/A', 'link': '#'}
                
                history.append({
                    'Time': timestamp_str,
                    'Input Snippet': item['user_input'][:30] + '...',
                    'Mood': item['detected_mood'].upper(),
                    'Song Title': song_data['song_title'],
                    'Artist': song_data['artists'],
                    'Link': song_data['link']
                })
            return history
        return []
    except Exception as e:
        st.error(f"Error fetching history: {e}")
        return []
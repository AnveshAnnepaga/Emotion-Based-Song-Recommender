from supabase_client import supabase

def log_user_interaction(user_input: str, detected_mood: str, recommended_song_id: int):
    """
    Logs a user's interaction and song recommendation to the database.
    
    :param user_input: The raw text provided by the user.
    :param detected_mood: The mood classified by the emotion analyzer.
    :param recommended_song_id: The ID of the song that was recommended.
    """
    try:
        user_id = 1
        
        data_to_log = {
            "user_id": user_id,
            "song_id": recommended_song_id,
            "user_input": user_input,
            "detected_mood": detected_mood
        }
        
        response = supabase.table("user_recommendations").insert(data_to_log).execute()
        
        if response.data:
            print("Chatbot: Your interaction has been logged for future improvements. 👍")
        else:
            print("Chatbot: Failed to log interaction.")
            
    except Exception as e:
        print(f"Chatbot: An error occurred while logging the interaction: {e}")
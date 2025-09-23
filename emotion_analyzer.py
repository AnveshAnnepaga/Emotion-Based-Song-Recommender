from textblob import TextBlob

def analyze_emotion(text: str) -> str:
    """
    Analyzes the user's input and maps it to a specific emotion
    (happy, calm, sad, angry, neutral, fear, surprise) using a hybrid approach.
    :param text: User's input string.
    :return: A string representing the detected emotion.
    """
    if not text:
        return 'neutral'

    # Convert the text to lowercase for case-insensitive matching
    lower_text = text.lower()
    
    # 1. Keyword-based emotion detection for specific moods
    # This is the primary method for emotions not covered by polarity.
    anger_keywords = ['angry', 'furious', 'annoyed', 'frustrated', 'rage', 'mad', 'irritated']
    calm_keywords = ['calm', 'peaceful', 'relaxed', 'tranquil', 'chill', 'serene']
    fear_keywords = ['anxious', 'scared', 'afraid', 'fear', 'terrified', 'anxiety', 'panic']
    surprise_keywords = ['surprised', 'shocked', 'stunned', 'amazed', 'unexpected']

    if any(word in lower_text for word in anger_keywords):
        return 'angry'
    elif any(word in lower_text for word in calm_keywords):
        return 'calm'
    elif any(word in lower_text for word in fear_keywords):
        return 'fear'
    elif any(word in lower_text for word in surprise_keywords):
        return 'surprise'

    # 2. Polarity-based emotion detection for happy, sad, and neutral
    # This is the fallback method if no specific keywords are found.
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    
    if polarity > 0.4:
        return 'happy'
    elif polarity < -0.4:
        return 'sad'
    else:
        return 'neutral'
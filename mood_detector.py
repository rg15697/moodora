"""
Mood Detection Module
Handles sentiment analysis and mood classification
"""

from textblob import TextBlob
from config import Config


class MoodDetector:
    """Class for detecting and classifying user moods"""
    
    def __init__(self):
        self.tmdb_genre_ids = Config.TMDB_GENRE_IDS
        self.mood_genres = Config.MOOD_GENRES
    
    def detect_mood(self, text: str) -> str:
        """
        Detect mood from user input text
        
        Args:
            text (str): User's mood description
            
        Returns:
            str: Detected mood category
        """
        if not text or not text.strip():
            return "thoughtful"
        
        polarity = TextBlob(text).sentiment.polarity
        text_lower = text.lower().strip()
        
        # Check for specific mood keywords first (expanded list)
        
        # Positive moods
        if any(word in text_lower for word in ["happy", "joy", "cheerful", "playful", "celebratory", "amused", "entertained"]):
            return "happy"
        if any(word in text_lower for word in ["excited", "energetic", "thrilled", "adrenaline", "pumped", "intense"]):
            return "excited"
        if any(word in text_lower for word in ["adventurous", "adventure", "explore", "journey"]):
            return "adventurous"
        if any(word in text_lower for word in ["inspired", "motivated", "hopeful", "optimistic"]):
            return "inspired"
        if any(word in text_lower for word in ["romantic", "love", "romance", "warm", "intimate"]):
            return "romantic"
        if any(word in text_lower for word in ["nostalgic", "nostalgia", "memories", "remember"]):
            return "nostalgic"
        
        # Negative moods
        if any(word in text_lower for word in ["sad", "depressed", "melancholy", "lonely", "pessimistic"]):
            return "sad"
        if any(word in text_lower for word in ["angry", "furious", "mad", "frustrated", "stressed"]):
            return "angry"
        if any(word in text_lower for word in ["scared", "fear", "horror", "terrified", "anxious", "afraid"]):
            return "scared"
        
        # Neutral/Complex moods
        if any(word in text_lower for word in ["curious", "wonder", "question", "learn", "discover"]):
            return "curious"
        if any(word in text_lower for word in ["thoughtful", "contemplative", "reflective", "creative", "focused"]):
            return "thoughtful"
        if any(word in text_lower for word in ["mysterious", "mystery", "suspenseful", "suspense"]):
            return "mysterious"
        if any(word in text_lower for word in ["calm", "peaceful", "meditative", "zen", "relaxed"]):
            return "calm"
        
        # Entertainment moods
        if any(word in text_lower for word in ["bored", "lazy", "silly", "witty", "sarcastic"]):
            return "bored"
        
        # Thrill-seeking moods
        if any(word in text_lower for word in ["dramatic", "tense", "thrilling"]):
            return "thrilled"
        
        # Fantasy/Escape moods
        if any(word in text_lower for word in ["dreamy", "magical", "whimsical", "escapist", "imaginative", "fantasy"]):
            return "dreamy"
        
        # Social moods
        if any(word in text_lower for word in ["social", "party", "festive", "friendly", "gathering"]):
            return "social"
        
        # Fallback to sentiment analysis
        if polarity > 0.5:
            return "happy"
        elif polarity < -0.3:
            return "sad"
        else:
            return "thoughtful"  # Better default than romantic
    
    def get_genre_id(self, mood: str) -> int:
        """
        Get TMDb genre ID for a given mood
        
        Args:
            mood (str): Detected mood
            
        Returns:
            int: TMDb genre ID
        """
        return self.tmdb_genre_ids.get(mood, 18)  # Default to Drama
    
    def get_fallback_genre(self, mood: str) -> str:
        """
        Get OMDb fallback genre keyword for a given mood
        
        Args:
            mood (str): Detected mood
            
        Returns:
            str: OMDb genre keyword
        """
        return self.mood_genres.get(mood, "drama")  # Default to drama
    
    def is_valid_mood(self, mood: str) -> bool:
        """
        Check if a mood is supported
        
        Args:
            mood (str): Mood to check
            
        Returns:
            bool: True if mood is supported
        """
        return mood in self.tmdb_genre_ids

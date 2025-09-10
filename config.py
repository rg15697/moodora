"""
Configuration module for Movie Mood App
Handles environment variables and app settings
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Application configuration class"""
    
    # API Keys
    OMDB_API_KEY = os.getenv("OMDB_API_KEY")
    # YouTube key loaded only from environment (no hardcoded fallback)
    YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
    TMDB_API_KEY = os.getenv("TMDB_API_KEY")

    
    # App Settings
    DEBUG = os.getenv("DEBUG", "True").lower() == "true"
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
    
    # API Settings
    REQUEST_TIMEOUT = 5
    MAX_MOVIES_PER_PAGE = 5
    MAX_PAGES = 10
    
    # TMDb Genre IDs mapping
    TMDB_GENRE_IDS = {
        # Positive moods
        "happy": 35,           # Comedy
        "excited": 28,         # Action
        "adventurous": 12,     # Adventure
        "inspired": 18,        # Drama
        "romantic": 10749,     # Romance
        "nostalgic": 18,       # Drama
        "hopeful": 18,         # Drama
        "energetic": 28,       # Action
        "playful": 35,         # Comedy
        "celebratory": 35,     # Comedy
        
        # Negative moods
        "sad": 18,             # Drama
        "angry": 28,           # Action
        "scared": 27,          # Horror
        "anxious": 27,         # Horror
        "depressed": 18,       # Drama
        "frustrated": 28,      # Action
        "lonely": 18,          # Drama
        "stressed": 28,        # Action
        "melancholy": 18,      # Drama
        "pessimistic": 18,     # Drama
        
        # Neutral/Complex moods
        "curious": 99,         # Documentary
        "thoughtful": 18,      # Drama
        "mysterious": 9648,    # Mystery
        "contemplative": 18,   # Drama
        "reflective": 18,      # Drama
        "creative": 18,        # Drama
        "focused": 99,         # Documentary
        "calm": 18,            # Drama
        "peaceful": 18,        # Drama
        "meditative": 18,      # Drama
        
        # Entertainment moods
        "bored": 35,           # Comedy
        "lazy": 35,            # Comedy
        "silly": 35,           # Comedy
        "witty": 35,           # Comedy
        "sarcastic": 35,       # Comedy
        "cheerful": 35,        # Comedy
        "amused": 35,          # Comedy
        "entertained": 35,     # Comedy
        
        # Thrill-seeking moods
        "thrilled": 28,        # Action
        "adrenaline": 28,      # Action
        "pumped": 28,          # Action
        "intense": 28,         # Action
        "dramatic": 18,        # Drama
        "suspenseful": 9648,   # Mystery
        "tense": 28,           # Action
        
        # Fantasy/Escape moods
        "dreamy": 14,          # Fantasy
        "magical": 14,         # Fantasy
        "whimsical": 14,       # Fantasy
        "escapist": 14,        # Fantasy
        "imaginative": 14,     # Fantasy
        "wonder": 14,          # Fantasy
        
        # Social moods
        "social": 35,          # Comedy
        "party": 35,           # Comedy
        "festive": 35,         # Comedy
        "friendly": 35,        # Comedy
        "warm": 10749,         # Romance
        "intimate": 10749,     # Romance
    }
    
    # Fallback OMDb keywords for when TMDb is not available
    MOOD_GENRES = {
        # Positive moods
        "happy": "comedy", "excited": "action", "adventurous": "adventure", "inspired": "drama",
        "romantic": "romance", "nostalgic": "drama", "hopeful": "drama", "energetic": "action",
        "playful": "comedy", "celebratory": "comedy",
        
        # Negative moods
        "sad": "drama", "angry": "action", "scared": "horror", "anxious": "horror",
        "depressed": "drama", "frustrated": "action", "lonely": "drama", "stressed": "action",
        "melancholy": "drama", "pessimistic": "drama",
        
        # Neutral/Complex moods
        "curious": "documentary", "thoughtful": "drama", "mysterious": "mystery", "contemplative": "drama",
        "reflective": "drama", "creative": "drama", "focused": "documentary", "calm": "drama",
        "peaceful": "drama", "meditative": "drama",
        
        # Entertainment moods
        "bored": "comedy", "lazy": "comedy", "silly": "comedy", "witty": "comedy",
        "sarcastic": "comedy", "cheerful": "comedy", "amused": "comedy", "entertained": "comedy",
        
        # Thrill-seeking moods
        "thrilled": "action", "adrenaline": "action", "pumped": "action", "intense": "action",
        "dramatic": "drama", "suspenseful": "mystery", "tense": "action",
        
        # Fantasy/Escape moods
        "dreamy": "fantasy", "magical": "fantasy", "whimsical": "fantasy", "escapist": "fantasy",
        "imaginative": "fantasy", "wonder": "fantasy",
        
        # Social moods
        "social": "comedy", "party": "comedy", "festive": "comedy", "friendly": "comedy",
        "warm": "romance", "intimate": "romance"
    }

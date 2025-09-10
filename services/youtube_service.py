"""
YouTube API Service
Handles trailer searches using YouTube API
"""

from urllib.parse import urlencode
from .base_service import BaseAPIService
from config import Config


class YouTubeService(BaseAPIService):
    """Service for YouTube API operations"""
    
    def __init__(self):
        super().__init__()
        self.api_key = Config.YOUTUBE_API_KEY
        self.base_url = "https://www.googleapis.com/youtube/v3/search"
    
    def get_trailer_url(self, title: str) -> str:
        """
        Get YouTube trailer URL for a movie title
        
        Args:
            title (str): Movie title
            
        Returns:
            str: YouTube trailer URL or None if not found
        """
        if not title or not self.validate_api_key(self.api_key, "YouTube"):
            return None
        
        # Check if API key is placeholder value
        if not self.api_key or self.api_key == "your_youtube_api_key":
            print("Warning: YouTube API key is not configured. Please set YOUTUBE_API_KEY in your .env file.")
            return None
        
        query = f"{title} trailer"
        params = {
            "part": "snippet",
            "q": query,
            "key": self.api_key,
            "type": "video",
            "maxResults": 1,
        }
        
        url = f"{self.base_url}?{urlencode(params)}"
        data = self.safe_request(url)
        
        if data.get("items"):
            video_id = data["items"][0]["id"]["videoId"]
            return f"https://www.youtube.com/watch?v={video_id}"
        
        return None
    
    def is_available(self) -> bool:
        """
        Check if YouTube service is available (has API key)
        
        Returns:
            bool: True if service is available
        """
        return bool(self.api_key)

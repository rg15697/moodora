"""
OMDb API Service
Handles movie searches and details from OMDb API
"""

from .base_service import BaseAPIService
from config import Config


class OMDbService(BaseAPIService):
    """Service for OMDb API operations"""
    
    def __init__(self):
        super().__init__()
        self.api_key = Config.OMDB_API_KEY
        self.base_url = "https://www.omdbapi.com/"
    
    def search_movies_by_name(self, movie_name: str) -> list:
        """
        Search movies by name using OMDb API
        
        Args:
            movie_name (str): Movie name to search
            
        Returns:
            list: List of movie search results
        """
        if not self.validate_api_key(self.api_key, "OMDb"):
            return []
        
        url = f"{self.base_url}?apikey={self.api_key}&s={movie_name}"
        data = self.safe_request(url)
        return data.get("Search", [])
    
    def search_movies_by_genre(self, genre_keyword: str) -> list:
        """
        Search movies by genre keyword using OMDb API
        
        Args:
            genre_keyword (str): Genre keyword to search
            
        Returns:
            list: List of movie search results
        """
        if not self.validate_api_key(self.api_key, "OMDb"):
            return []
        
        url = f"{self.base_url}?apikey={self.api_key}&s={genre_keyword}"
        data = self.safe_request(url)
        return data.get("Search", [])
    
    def get_movie_details(self, imdb_id: str) -> dict:
        """
        Get detailed movie information by IMDb ID
        
        Args:
            imdb_id (str): IMDb ID of the movie
            
        Returns:
            dict: Movie details
        """
        if not self.validate_api_key(self.api_key, "OMDb"):
            return {}
        
        url = f"{self.base_url}?apikey={self.api_key}&i={imdb_id}&plot=short"
        return self.safe_request(url)
    
    def is_available(self) -> bool:
        """
        Check if OMDb service is available (has API key)
        
        Returns:
            bool: True if service is available
        """
        return bool(self.api_key)

"""
TMDb API Service
Handles movie searches and details from TMDb API
"""

from .base_service import BaseAPIService
from config import Config


class TMDbService(BaseAPIService):
    """Service for TMDb API operations"""
    
    def __init__(self):
        super().__init__()
        self.api_key = Config.TMDB_API_KEY
        self.base_url = "https://api.themoviedb.org/3"
        self.image_base_url = "https://image.tmdb.org/t/p/w500"
    
    def search_movies_by_genre(self, genre_id: int, page: int = 1) -> list:
        """
        Search movies by genre ID using TMDb API
        
        Args:
            genre_id (int): TMDb genre ID
            page (int): Page number for pagination
            
        Returns:
            list: List of movie search results
        """
        if not self.validate_api_key(self.api_key, "TMDb"):
            return []
        
        url = f"{self.base_url}/discover/movie?api_key={self.api_key}&with_genres={genre_id}&sort_by=popularity.desc&page={page}"
        data = self.safe_request(url)
        return data.get("results", [])
    
    def get_movie_details(self, tmdb_id: int) -> dict:
        """
        Get detailed movie information by TMDb ID
        
        Args:
            tmdb_id (int): TMDb ID of the movie
            
        Returns:
            dict: Movie details
        """
        if not self.validate_api_key(self.api_key, "TMDb"):
            return {}
        
        url = f"{self.base_url}/movie/{tmdb_id}?api_key={self.api_key}"
        return self.safe_request(url)
    
    def get_total_pages(self, genre_id: int, page: int = 1) -> int:
        """
        Get total pages available for a genre search
        
        Args:
            genre_id (int): TMDb genre ID
            page (int): Page number to check
            
        Returns:
            int: Total pages available
        """
        if not self.validate_api_key(self.api_key, "TMDb"):
            return 1
        
        url = f"{self.base_url}/discover/movie?api_key={self.api_key}&with_genres={genre_id}&sort_by=popularity.desc&page={page}"
        data = self.safe_request(url)
        total_pages = data.get("total_pages", 1)
        return min(total_pages, Config.MAX_PAGES)  # Limit to max pages
    
    def format_movie_data(self, tmdb_movie: dict) -> dict:
        """
        Format TMDb movie data for template compatibility
        
        Args:
            tmdb_movie (dict): Raw TMDb movie data
            
        Returns:
            dict: Formatted movie data
        """
        details = self.get_movie_details(tmdb_movie["id"])
        if not details:
            return {}
        
        return {
            "Title": details.get("title", ""),
            "Year": details.get("release_date", "")[:4] if details.get("release_date") else "",
            "Plot": details.get("overview", ""),
            "Poster": f"{self.image_base_url}{details.get('poster_path', '')}" if details.get("poster_path") else "N/A",
            "imdbID": details.get("imdb_id", ""),
            "tmdb_id": details.get("id", "")
        }
    
    def is_available(self) -> bool:
        """
        Check if TMDb service is available (has API key)
        
        Returns:
            bool: True if service is available
        """
        return bool(self.api_key)

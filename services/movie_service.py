"""
Movie Service
Orchestrates movie searches across different APIs
"""

from .omdb_service import OMDbService
from .tmdb_service import TMDbService
from .youtube_service import YouTubeService
from mood_detector import MoodDetector
from config import Config


class MovieService:
    """Main service for movie operations"""
    
    def __init__(self):
        self.omdb_service = OMDbService()
        self.tmdb_service = TMDbService()
        self.youtube_service = YouTubeService()
        self.mood_detector = MoodDetector()
    
    def search_by_name(self, movie_name: str) -> list:
        """
        Search movies by name using OMDb
        
        Args:
            movie_name (str): Movie name to search
            
        Returns:
            list: List of movie results
        """
        if not movie_name or not movie_name.strip():
            return []
        
        movies = self.omdb_service.search_movies_by_name(movie_name.strip())
        return self._add_trailers(movies)
    
    def search_by_mood(self, description: str, page: int = 1) -> tuple:
        """
        Search movies by mood using TMDb with OMDb fallback
        
        Args:
            description (str): Mood description
            page (int): Page number for pagination
            
        Returns:
            tuple: (movies_list, total_pages)
        """
        if not description or not description.strip():
            return [], 1
        
        mood = self.mood_detector.detect_mood(description.strip())
        print(f"DEBUG: Input: '{description}' -> Detected mood: '{mood}'")
        
        movies = []
        total_pages = 1
        
        # Try TMDb first for better genre filtering
        if self.tmdb_service.is_available() and self.mood_detector.is_valid_mood(mood):
            genre_id = self.mood_detector.get_genre_id(mood)
            print(f"DEBUG: Using TMDb genre ID {genre_id} for mood '{mood}'")
            
            tmdb_movies = self.tmdb_service.search_movies_by_genre(genre_id, page)
            if tmdb_movies:
                movies = []
                for tmdb_movie in tmdb_movies[:Config.MAX_MOVIES_PER_PAGE]:
                    formatted_movie = self.tmdb_service.format_movie_data(tmdb_movie)
                    if formatted_movie:
                        movies.append(formatted_movie)
                
                # Add trailers to TMDb movies
                movies = self._add_trailers(movies)
                total_pages = self.tmdb_service.get_total_pages(genre_id, page)
        
        # Fallback to OMDb if TMDb fails or no API key
        if not movies and self.omdb_service.is_available():
            genre_keyword = self.mood_detector.get_fallback_genre(mood)
            movies = self.omdb_service.search_movies_by_genre(genre_keyword)
            movies = self._add_trailers(movies)
        
        return movies, total_pages
    
    def _add_trailers(self, movies: list) -> list:
        """
        Add YouTube trailers to movie list
        
        Args:
            movies (list): List of movies
            
        Returns:
            list: Movies with trailers added
        """
        if not movies:
            return movies
        
        if not self.youtube_service.is_available():
            return movies
        
        detailed_movies = []
        for movie in movies:
            if movie.get("tmdb_id"):
                # TMDb data - add trailer directly
                title = movie.get("Title", "")
                trailer_url = self.youtube_service.get_trailer_url(title)
                movie["trailer"] = trailer_url
                detailed_movies.append(movie)
            elif movie.get("imdbID"):
                # OMDb data - get details and add trailer
                details = self.omdb_service.get_movie_details(movie.get("imdbID"))
                if details:
                    title = details.get("Title", "")
                    trailer_url = self.youtube_service.get_trailer_url(title)
                    details["trailer"] = trailer_url
                    detailed_movies.append(details)
        
        return detailed_movies
    
    def get_available_services(self) -> dict:
        """
        Get status of available services
        
        Returns:
            dict: Service availability status
        """
        return {
            "omdb": self.omdb_service.is_available(),
            "tmdb": self.tmdb_service.is_available(),
            "youtube": self.youtube_service.is_available()
        }

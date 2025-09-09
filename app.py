"""
Movie Mood Recommender App
Main Flask application with refactored modular structure
"""

from flask import Flask, render_template, request
from services.movie_service import MovieService
from config import Config


def create_app():
    """Create and configure Flask application"""
    app = Flask(__name__)
    app.config['SECRET_KEY'] = Config.SECRET_KEY
    app.config['DEBUG'] = Config.DEBUG
    
    # Initialize services
    movie_service = MovieService()
    
    @app.route("/", methods=["GET", "POST"])
    def home():
        """Main route for movie search"""
        movies = None
        error = None
        current_page = 1
        total_pages = 1
        search_params = {}
        
        # Handle pagination for GET requests
        if request.method == "GET" and request.args.get("page"):
            current_page = int(request.args.get("page", 1))
            choice = request.args.get("choice")
            search_params = {
                "choice": choice,
                "movie_name": request.args.get("movie_name", ""),
                "description": request.args.get("description", "")
            }
        
        # Process search requests
        if request.method == "POST" or (request.method == "GET" and request.args.get("page")):
            choice = request.form.get("choice") or request.args.get("choice")
            
            if choice == "name":
                movie_name = (request.form.get("movie_name") or request.args.get("movie_name") or "").strip()
                if not movie_name:
                    error = "Please enter a movie name."
                else:
                    if not movie_service.omdb_service.is_available():
                        error = "OMDB_API_KEY is missing. Please configure your .env."
                    else:
                        movies = movie_service.search_by_name(movie_name)
                        search_params = {"choice": "name", "movie_name": movie_name}
            
            elif choice == "mood":
                description = (request.form.get("description") or request.args.get("description") or "").strip()
                if not description:
                    error = "Please describe your mood."
                else:
                    search_params = {"choice": "mood", "description": description}
                    
                    # Check if any service is available
                    services = movie_service.get_available_services()
                    if not services["omdb"] and not services["tmdb"]:
                        error = "TMDB_API_KEY or OMDB_API_KEY is missing. Please configure your .env."
                    else:
                        movies, total_pages = movie_service.search_by_mood(description, current_page)
        
        return render_template("index.html", 
                             movies=movies, 
                             error=error, 
                             current_page=current_page,
                             total_pages=total_pages,
                             search_params=search_params)
    
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=Config.DEBUG)
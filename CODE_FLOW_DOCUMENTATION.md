# Movie Mood Recommender App - Code Flow Documentation

## Table of Contents
1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Code Flow](#code-flow)
4. [Module Details](#module-details)
5. [API Integration Flow](#api-integration-flow)
6. [Data Flow](#data-flow)
7. [Error Handling](#error-handling)
8. [Configuration](#configuration)

## Overview

The Movie Mood Recommender App is a Flask web application that recommends movies based on user moods using TMDb and OMDb APIs. The application follows a modular architecture with clear separation of concerns.

## Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Flask App     │    │   Services      │
│   (HTML/CSS/JS) │◄──►│   (app.py)      │◄──►│   Layer         │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │   External      │
                       │   APIs          │
                       │   (TMDb/OMDb/   │
                       │   YouTube)      │
                       └─────────────────┘
```

## Code Flow

### 1. Application Startup
```
app.py (create_app())
├── Load configuration from config.py
├── Initialize services
│   ├── OMDbService
│   ├── TMDbService
│   ├── YouTubeService
│   └── MovieService (orchestrator)
└── Register routes
```

### 2. User Request Flow
```
User Input → Flask Route → Service Layer → External APIs → Response
```

#### Detailed Flow:
1. **User visits homepage** → `GET /`
2. **User submits form** → `POST /` or `GET /?page=X`
3. **Route handler** → `home()` function in `app.py`
4. **Service orchestration** → `MovieService` methods
5. **API calls** → TMDb/OMDb/YouTube services
6. **Response rendering** → Template with movie data

## Module Details

### 1. `app.py` - Main Flask Application
```python
# Key Functions:
create_app()           # Application factory
home()                 # Main route handler
```

**Responsibilities:**
- Flask application setup
- Route handling
- Request/response management
- Service orchestration

### 2. `config.py` - Configuration Management
```python
# Key Classes:
Config                 # Configuration container
```

**Responsibilities:**
- Environment variable loading
- API key management
- App settings (timeouts, limits)
- Genre mappings (TMDb IDs, OMDb keywords)

### 3. `mood_detector.py` - Mood Detection
```python
# Key Classes:
MoodDetector          # Mood detection and classification

# Key Methods:
detect_mood(text)     # Main mood detection
get_genre_id(mood)    # Get TMDb genre ID
get_fallback_genre(mood) # Get OMDb keyword
is_valid_mood(mood)   # Validate mood support
```

**Responsibilities:**
- Text sentiment analysis
- Mood keyword recognition
- Genre mapping
- Fallback handling

### 4. `services/` - API Service Layer

#### `base_service.py` - Base API Service
```python
# Key Classes:
BaseAPIService        # Common API functionality

# Key Methods:
safe_request(url)     # HTTP request with error handling
validate_api_key()    # API key validation
```

#### `omdb_service.py` - OMDb API Integration
```python
# Key Methods:
search_movies_by_name()    # Search by movie title
search_movies_by_genre()   # Search by genre keyword
get_movie_details()        # Get detailed movie info
is_available()            # Check API availability
```

#### `tmdb_service.py` - TMDb API Integration
```python
# Key Methods:
search_movies_by_genre()   # Search by genre ID
get_movie_details()        # Get detailed movie info
get_total_pages()         # Get pagination info
format_movie_data()       # Format for template
is_available()           # Check API availability
```

#### `youtube_service.py` - YouTube API Integration
```python
# Key Methods:
get_trailer_url()        # Get YouTube trailer URL
is_available()          # Check API availability
```

#### `movie_service.py` - Main Orchestrator
```python
# Key Methods:
search_by_name()         # Search movies by name
search_by_mood()         # Search movies by mood
_add_trailers()          # Add YouTube trailers
get_available_services() # Check service status
```

## API Integration Flow

### Mood-Based Search Flow
```
User Input: "I feel happy"
    ↓
MoodDetector.detect_mood("I feel happy")
    ↓ Returns: "happy"
    ↓
MoodDetector.get_genre_id("happy")
    ↓ Returns: 35 (Comedy)
    ↓
TMDbService.search_movies_by_genre(35, page=1)
    ↓ Returns: [movie1, movie2, ...]
    ↓
TMDbService.format_movie_data(movie)
    ↓ Returns: {Title, Year, Plot, Poster, ...}
    ↓
YouTubeService.get_trailer_url(title)
    ↓ Returns: "https://youtube.com/watch?v=..."
    ↓
Template rendering with movie data
```

### Name-Based Search Flow
```
User Input: "The Matrix"
    ↓
OMDbService.search_movies_by_name("The Matrix")
    ↓ Returns: [movie1, movie2, ...]
    ↓
OMDbService.get_movie_details(imdb_id)
    ↓ Returns: {Title, Year, Plot, Poster, ...}
    ↓
YouTubeService.get_trailer_url(title)
    ↓ Returns: "https://youtube.com/watch?v=..."
    ↓
Template rendering with movie data
```

## Data Flow

### 1. Request Processing
```
HTTP Request
    ↓
Flask Route Handler
    ↓
Parameter Extraction (choice, movie_name, description, page)
    ↓
Service Selection (name vs mood)
    ↓
API Calls
    ↓
Data Processing
    ↓
Template Rendering
    ↓
HTTP Response
```

### 2. Data Transformation
```
Raw API Response
    ↓
Service Layer Processing
    ↓
Standardized Movie Object
    ↓
Template Data
    ↓
HTML Rendering
```

### 3. Movie Object Structure
```python
{
    "Title": "Movie Title",
    "Year": "2023",
    "Plot": "Movie description...",
    "Poster": "https://image.tmdb.org/t/p/w500/poster.jpg",
    "imdbID": "tt1234567",
    "tmdb_id": "12345",
    "trailer": "https://youtube.com/watch?v=abc123"
}
```

## Error Handling

### 1. API Error Handling
```python
# In base_service.py
def safe_request(url):
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return {}
```

### 2. Service Availability
```python
# Check if services are available
if not self.youtube_service.is_available():
    return movies  # Skip trailer addition
```

### 3. Fallback Strategy
```
TMDb API (Primary)
    ↓ (if fails)
OMDb API (Fallback)
    ↓ (if fails)
Error Message to User
```

## Configuration

### Environment Variables
```env
OMDB_API_KEY=your_omdb_key
YOUTUBE_API_KEY=your_youtube_key
TMDB_API_KEY=your_tmdb_key
DEBUG=True
SECRET_KEY=your_secret_key
```

### App Settings
```python
REQUEST_TIMEOUT = 5
MAX_MOVIES_PER_PAGE = 5
MAX_PAGES = 10
```

## Key Design Patterns

### 1. Service Layer Pattern
- Separates business logic from API calls
- Provides clean interfaces
- Enables easy testing and mocking

### 2. Factory Pattern
- `create_app()` function creates configured Flask app
- Allows for different configurations (dev, prod, test)

### 3. Strategy Pattern
- Different services for different APIs
- Fallback strategies for API failures

### 4. Template Method Pattern
- `BaseAPIService` provides common functionality
- Specific services implement specific behavior

## File Structure
```
movie_mood_app/
├── app.py                    # Main Flask application
├── config.py                 # Configuration management
├── mood_detector.py          # Mood detection logic
├── services/                 # API service layer
│   ├── __init__.py
│   ├── base_service.py       # Common API functionality
│   ├── omdb_service.py       # OMDb API integration
│   ├── tmdb_service.py       # TMDb API integration
│   ├── youtube_service.py    # YouTube API integration
│   └── movie_service.py      # Main orchestrator
├── templates/
│   └── index.html           # Main UI template
├── requirements.txt         # Python dependencies
├── README.md               # Project documentation
└── CODE_FLOW_DOCUMENTATION.md # This file
```

## Usage Examples

### 1. Adding a New Mood
```python
# In config.py
TMDB_GENRE_IDS = {
    "new_mood": 28,  # Action genre ID
    # ... existing moods
}

# In mood_detector.py
def detect_mood(text):
    if "new_mood_keyword" in text_lower:
        return "new_mood"
    # ... existing logic
```

### 2. Adding a New API Service
```python
# Create new_service.py
class NewService(BaseAPIService):
    def __init__(self):
        super().__init__()
        self.api_key = Config.NEW_API_KEY
    
    def search_movies(self, query):
        # Implementation
        pass

# Update movie_service.py
def __init__(self):
    self.new_service = NewService()
    # ... existing services
```

### 3. Modifying Movie Display
```python
# In template (index.html)
<div class="card-body">
    <h5 class="card-title">{{ movie.Title }}</h5>
    <p class="card-text">{{ movie.Plot }}</p>
    <p><strong>Year:</strong> {{ movie.Year }}</p>
    <!-- Add new fields here -->
    <p><strong>Rating:</strong> {{ movie.Rating }}</p>
</div>
```

This documentation provides a comprehensive understanding of the code flow and architecture of your Movie Mood Recommender App. Each module has a clear responsibility, and the flow is designed to be maintainable and extensible.

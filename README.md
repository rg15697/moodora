# Moodora – Mood & Context Based Movies recommender

A Flask web application that recommends movies based on your current mood using TMDb and OMDb APIs.

## Features

- **Mood-based Movie Recommendations**: 50+ supported moods with intelligent genre mapping
- **Dual API Integration**: TMDb for accurate genre filtering, OMDb as fallback
- **Interactive UI**: Clickable mood tags with beautiful gradients and animations
- **Pagination**: Browse through up to 5 movies per page with 10 pages max
- **YouTube Trailers**: Automatic trailer links for discovered movies
- **Responsive Design**: Works on desktop and mobile devices

## Project Structure

```
movie_mood_app/
├── app.py                 # Main Flask application
├── config.py             # Configuration and settings
├── mood_detector.py      # Mood detection and sentiment analysis
├── services/             # API service modules
│   ├── __init__.py
│   ├── base_service.py   # Base API service class
│   ├── omdb_service.py   # OMDb API integration
│   ├── tmdb_service.py   # TMDb API integration
│   ├── youtube_service.py # YouTube API integration
│   └── movie_service.py  # Main movie service orchestrator
├── templates/
│   └── index.html        # Main UI template
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## Setup

1. **Create and activate a virtual environment** (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Create a `.env` file** in the project root with your API keys:
```env
OMDB_API_KEY=your_omdb_api_key
YOUTUBE_API_KEY=your_youtube_api_key
TMDB_API_KEY=your_tmdb_api_key
DEBUG=True
SECRET_KEY=your-secret-key
```

4. **Run the application**:
```bash
python app.py
```

## API Keys

- **OMDb API**: Get your free key from [OMDb API](http://www.omdbapi.com/apikey.aspx)
- **TMDb API**: Get your free key from [TMDb API](https://www.themoviedb.org/settings/api)
- **YouTube API**: Get your key from [Google Cloud Console](https://console.cloud.google.com/)

## Supported Moods

The app supports 50+ moods across 6 categories:

- **Positive**: happy, excited, adventurous, inspired, romantic, nostalgic
- **Negative**: sad, angry, scared, anxious, depressed, frustrated
- **Neutral**: curious, thoughtful, mysterious, calm, contemplative
- **Entertainment**: bored, lazy, silly, witty, sarcastic
- **Thrill-seeking**: thrilled, adrenaline, pumped, intense, dramatic
- **Fantasy**: dreamy, magical, whimsical, escapist, imaginative
- **Social**: social, party, festive, friendly, warm

## Architecture

- **Modular Design**: Separated concerns into dedicated modules
- **Service Layer**: Clean API abstractions with error handling
- **Configuration Management**: Centralized settings and environment variables
- **Mood Detection**: Advanced sentiment analysis with keyword matching
- **Fallback Strategy**: Graceful degradation when APIs are unavailable

## Development

The codebase follows clean architecture principles:
- **Separation of Concerns**: Each module has a single responsibility
- **Dependency Injection**: Services are injected where needed
- **Error Handling**: Comprehensive error handling and logging
- **Type Hints**: Better code documentation and IDE support
- **Configuration**: Environment-based configuration management

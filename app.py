from flask import Flask, render_template, request
import requests
from textblob import TextBlob
import os

app = Flask(__name__)

# Load API Keys from environment variables
TMDB_API_KEY = os.getenv("TMDB_API_KEY")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

# Mood-to-genre mapping
MOOD_GENRES = {
    "happy": "35",       # Comedy
    "sad": "18",         # Drama
    "angry": "28",       # Action
    "romantic": "10749", # Romance
    "scared": "27"       # Horror
}

# Detect genre based on mood description
def get_sentiment_genre(text):
    polarity = TextBlob(text).sentiment.polarity
    text_lower = text.lower()

    # Explicit keyword detection
    if "angry" in text_lower or "furious" in text_lower:
        return MOOD_GENRES["angry"]
    if "scared" in text_lower or "fear" in text_lower:
        return MOOD_GENRES["scared"]
    if "love" in text_lower or "romantic" in text_lower:
        return MOOD_GENRES["romantic"]

    # Sentiment-based fallback
    if polarity > 0.5:
        return MOOD_GENRES["happy"]
    elif polarity < -0.3:
        return MOOD_GENRES["sad"]
    else:
        return MOOD_GENRES["romantic"]

def safe_request(url):
    try:
        resp = requests.get(url, timeout=5)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return {}

def search_movies_by_name(movie_name):
    url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={movie_name}"
    data = safe_request(url)
    return data.get("results", [])

def search_movies_by_genre(genre_id):
    url = f"https://api.themoviedb.org/3/discover/movie?api_key={TMDB_API_KEY}&with_genres={genre_id}&sort_by=popularity.desc"
    data = safe_request(url)
    return data.get("results", [])

def get_youtube_trailer(title):
    query = f"{title} trailer"
    url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={query}&key={YOUTUBE_API_KEY}&type=video&maxResults=1"
    data = safe_request(url)
    if data.get("items"):
        return f"https://www.youtube.com/watch?v={data['items'][0]['id']['videoId']}"
    return None

@app.route("/", methods=["GET", "POST"])
def home():
    movies = []
    if request.method == "POST":
        choice = request.form.get("choice")
        if choice == "name":
            movie_name = request.form.get("movie_name")
            movies = search_movies_by_name(movie_name)
        elif choice == "mood":
            description = request.form.get("description")
            genre_id = get_sentiment_genre(description)
            movies = search_movies_by_genre(genre_id)

        # Add YouTube trailers for top 5 results only
        for m in movies[:5]:
            m["trailer"] = get_youtube_trailer(m["title"])

    return render_template("index.html", movies=movies)

if __name__ == "__main__":
    app.run(debug=True)

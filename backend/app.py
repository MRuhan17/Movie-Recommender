import os
import requests
from typing import List
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(title="Movie Recommender API")

# CORS Configuration
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://mruhan17.github.io",
    "https://movie-recommender-mruhan17.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Get API Key
TMDB_API_KEY = os.getenv("TMDB_API_KEY")
if not TMDB_API_KEY:
    print("WARNING: TMDB_API_KEY not found in environment variables")

TMDB_BASE_URL = "https://api.themoviedb.org/3"


# Pydantic Models
class MovieAction(BaseModel):
    movie_id: int
    title: str
    genres: List[str]
    rating: float


class UserProfile(BaseModel):
    user_id: str
    watched: List[MovieAction] = []
    liked: List[MovieAction] = []


# Helper functions
def get_tmdb_data(endpoint: str, params: dict = None):
    """Fetch data from TMDB API"""
    if not TMDB_API_KEY:
        raise HTTPException(status_code=500, detail="TMDB API key not configured")

    params = params or {}
    params["api_key"] = TMDB_API_KEY

    response = requests.get(f"{TMDB_BASE_URL}{endpoint}", params=params)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="TMDB API error")

    return response.json()


@app.get("/")
async def root():
    return {"message": "Movie Recommender API", "status": "running"}


@app.get("/health_check")
async def health_check():
    return {"status": "healthy"}


@app.get("/api/movies/trending")
async def get_trending(page: int = 1):
    """Get trending movies from TMDB"""
    try:
        data = get_tmdb_data("/trending/movie/week", {"page": page})
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/movies/search")
async def search_movies(query: str, page: int = 1):
    """Search for movies"""
    try:
        data = get_tmdb_data("/search/movie", {"query": query, "page": page})
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/recommendations/default")
async def get_default_recommendations(top_n: int = 10):
    """Get default recommendations for anonymous users"""
    try:
        # Return popular movies as default recommendations
        data = get_tmdb_data("/movie/popular", {"page": 1})
        results = data.get("results", [])[:top_n]
        return {"recommendations": results, "method": "popular"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/recommendations/{user_id}")
async def get_recommendations(user_id: str, top_n: int = 10):
    """Get personalized recommendations (simplified - returns popular movies)"""
    try:
        # For now, return popular movies as recommendations
        data = get_tmdb_data("/movie/popular", {"page": 1})
        results = data.get("results", [])[:top_n]
        return {"recommendations": results, "method": "popular"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/explain/{user_id}/{movie_id}")
async def explain_recommendation(user_id: str, movie_id: int):
    """Explain why a movie is recommended (simplified)"""
    try:
        # Get movie details
        movie_data = get_tmdb_data(f"/movie/{movie_id}")

        return {
            "movie_id": movie_id,
            "title": movie_data.get("title"),
            "explanation": "This movie is popular and highly rated.",
            "genres": [g["name"] for g in movie_data.get("genres", [])],
            "rating": movie_data.get("vote_average"),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/history/add")
async def add_to_history(action: MovieAction):
    """Add movie to user history (simplified - just returns success)"""
    return {"status": "success", "message": "History tracking coming soon"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

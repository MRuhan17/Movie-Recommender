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
USE_MOCK_DATA = not TMDB_API_KEY
if not TMDB_API_KEY:
    print("WARNING: TMDB_API_KEY not found in environment variables")
    print("INFO: Using mock data for development")

TMDB_BASE_URL = "https://api.themoviedb.org/3"

# Mock movie data for development when TMDB API key is not available
MOCK_MOVIES = {
    "results": [
        {
            "id": 1,
            "title": "The Shawshank Redemption",
            "poster_path": "/q6y0Go1tsGEsmtFryDOJo3dEmqu.jpg",
            "vote_average": 8.7,
            "overview": "Framed in the 1940s for the double murder of his wife and her lover, upstanding banker Andy Dufresne begins a new life at the Shawshank prison, where he puts his accounting skills to work for an amoral warden.",
            "release_date": "1994-09-23",
            "genres": ["Drama", "Crime"]
        },
        {
            "id": 2,
            "title": "The Godfather",
            "poster_path": "/3bhkrj58Vtu7enYsRolD1fZdja1.jpg",
            "vote_average": 8.7,
            "overview": "Spanning the years 1945 to 1955, a chronicle of the fictional Italian-American Corleone crime family.",
            "release_date": "1972-03-14",
            "genres": ["Drama", "Crime"]
        },
        {
            "id": 3,
            "title": "The Dark Knight",
            "poster_path": "/qJ2tW6WMUDux911r6m7haRef0WH.jpg",
            "vote_average": 8.5,
            "overview": "Batman raises the stakes in his war on crime with the help of Lt. Jim Gordon and District Attorney Harvey Dent.",
            "release_date": "2008-07-16",
            "genres": ["Action", "Crime", "Drama"]
        },
        {
            "id": 4,
            "title": "Pulp Fiction",
            "poster_path": "/d5iIlFn5s0ImszYzBPb8JPIfbXD.jpg",
            "vote_average": 8.5,
            "overview": "A burger-loving hit man, his philosophical partner, a drug-addled gangster's moll and a washed-up boxer converge in this sprawling crime comedy.",
            "release_date": "1994-09-10",
            "genres": ["Crime", "Drama"]
        },
        {
            "id": 5,
            "title": "Forrest Gump",
            "poster_path": "/arw2vcBveWOVZr6pxd9XTd1TdQa.jpg",
            "vote_average": 8.5,
            "overview": "A man with a low IQ has accomplished great things in his life and been present during significant historic events.",
            "release_date": "1994-06-23",
            "genres": ["Comedy", "Drama", "Romance"]
        },
        {
            "id": 6,
            "title": "Inception",
            "poster_path": "/9gk7adHYeDvHkCSEqAvQNLV5Uge.jpg",
            "vote_average": 8.4,
            "overview": "Cobb, a skilled thief who commits corporate espionage by infiltrating the subconscious of his targets is offered a chance to regain his old life.",
            "release_date": "2010-07-15",
            "genres": ["Action", "Science Fiction", "Adventure"]
        },
        {
            "id": 7,
            "title": "Fight Club",
            "poster_path": "/pB8BM7pdSp6B6Ih7QZ4DrQ3PmJK.jpg",
            "vote_average": 8.4,
            "overview": "A ticking-time-bomb insomniac and a slippery soap salesman channel primal male aggression into a shocking new form of therapy.",
            "release_date": "1999-10-15",
            "genres": ["Drama"]
        },
        {
            "id": 8,
            "title": "The Matrix",
            "poster_path": "/f89U3ADr1oiB1s9GkdPOEpXUk5H.jpg",
            "vote_average": 8.2,
            "overview": "Set in the 22nd century, The Matrix tells the story of a computer hacker who joins a group of underground insurgents fighting the vast and powerful computers who now rule the earth.",
            "release_date": "1999-03-30",
            "genres": ["Action", "Science Fiction"]
        },
        {
            "id": 9,
            "title": "Goodfellas",
            "poster_path": "/aKuFiU82s5ISJpGZp7YkIr3kCUd.jpg",
            "vote_average": 8.5,
            "overview": "The story of Henry Hill and his life in the mob, covering his relationship with his wife Karen Hill and his mob partners.",
            "release_date": "1990-09-12",
            "genres": ["Drama", "Crime"]
        },
        {
            "id": 10,
            "title": "Interstellar",
            "poster_path": "/gEU2QniE6E77NI6lCU6MxlNBvIx.jpg",
            "vote_average": 8.4,
            "overview": "The adventures of a group of explorers who make use of a newly discovered wormhole to surpass the limitations on human space travel.",
            "release_date": "2014-11-05",
            "genres": ["Adventure", "Drama", "Science Fiction"]
        }
    ],
    "page": 1,
    "total_pages": 1,
    "total_results": 10
}


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
    """Fetch data from TMDB API or return mock data"""
    if USE_MOCK_DATA:
        # Return mock data for development
        print(f"INFO: Returning mock data for endpoint: {endpoint}")
        return MOCK_MOVIES.copy()
    
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


@app.get("/api/debug")
async def debug_status():
    """Check if API key is configured"""
    return {
        "use_mock_data": USE_MOCK_DATA,
        "api_key_found": bool(TMDB_API_KEY),
        "api_key_length": len(TMDB_API_KEY) if TMDB_API_KEY else 0,
        "env_vars": list(os.environ.keys())
    }


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

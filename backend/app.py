import os
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

# Import from the nested backend package
# Assuming running from root as: uvicorn backend.app:app
from backend.backend.user_history import UserHistoryManager, PersonalizedRecommender
from backend.backend.tmdb_recommender import TMDBFusion, HybridRecommender
from backend.backend.explainable_recommender import ExplainableRecommender

# Load environment variables
load_dotenv()

app = FastAPI(title="Movie Recommender API")

# CORS Configuration
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Components
# Ensure models directory exists for any local models
os.makedirs("models", exist_ok=True)

# Get API Key
TMDB_API_KEY = os.getenv("TMDB_API_KEY")
if not TMDB_API_KEY:
    print("WARNING: TMDB_API_KEY not found in environment variables.")

# Initialize Managers
# We use a singleton pattern-like approach here for simplicity
history_manager = UserHistoryManager()
tmdb_fusion = TMDBFusion(api_key=TMDB_API_KEY)
personalized_recommender = PersonalizedRecommender(history_manager)
hybrid_recommender = HybridRecommender(tmdb_fusion, personalized_recommender)
explainable_recommender = ExplainableRecommender(history_manager, tmdb_fusion)

# --- Pydantic Models ---

class MovieAction(BaseModel):
    movie_id: int
    title: str
    genres: List[str]
    rating: Optional[float] = None

class UserProfile(BaseModel):
    user_id: str

# --- Endpoints ---

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/api/movies/trending")
async def get_trending(page: int = 1):
    """Get trending movies from TMDB"""
    try:
        return hybrid_recommender._get_trending_movies(page=page)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/movies/search")
async def search_movies(query: str, page: int = 1):
    """Search for movies"""
    try:
        return tmdb_fusion.search_movies(query, page=page)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/recommendations/{user_id}")
async def get_recommendations(user_id: str, top_n: int = 10):
    """Get personalized recommendations"""
    try:
        return hybrid_recommender.get_smart_recommendations(user_id, top_n=top_n)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/explain/{user_id}/{movie_id}")
async def explain_recommendation(user_id: str, movie_id: int):
    """Explain why a movie was recommended"""
    try:
        # We need movie details to explain. 
        # In a real app, we might pass the movie object or fetch it.
        # Here we fetch it from TMDB.
        movie_details = tmdb_fusion.get_movie_details(movie_id)
        if not movie_details:
            raise HTTPException(status_code=404, detail="Movie not found")
        
        # Enrich it to match the format expected by explainer
        enriched_movie = tmdb_fusion.enrich_movie_data(movie_details)
        
        explanation = explainable_recommender.explain_recommendation(user_id, enriched_movie)
        return explanation
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/user/{user_id}/history")
async def get_history(user_id: str):
    """Get user watch history"""
    return history_manager.get_watch_history(user_id)

@app.post("/api/user/{user_id}/history")
async def add_to_history(user_id: str, action: MovieAction):
    """Add movie to watch history"""
    history_manager.add_to_history(
        user_id, 
        action.movie_id, 
        action.title, 
        action.genres, 
        action.rating
    )
    return {"status": "success"}

@app.get("/api/user/{user_id}/likes")
async def get_likes(user_id: str):
    """Get user liked movies"""
    return history_manager.get_liked_movies(user_id)

@app.post("/api/user/{user_id}/likes")
async def add_like(user_id: str, action: MovieAction):
    """Add movie to likes"""
    history_manager.add_like(
        user_id, 
        action.movie_id, 
        action.title, 
        action.genres
    )
    return {"status": "success"}

@app.delete("/api/user/{user_id}/likes/{movie_id}")
async def remove_like(user_id: str, movie_id: int):
    """Remove movie from likes"""
    history_manager.remove_like(user_id, movie_id)
    return {"status": "success"}

@app.get("/api/user/{user_id}/profile")
async def get_profile(user_id: str):
    """Get full user profile"""
    return history_manager.get_user_profile(user_id)

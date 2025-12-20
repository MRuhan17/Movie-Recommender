from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from typing import List, Optional
from backend.app.database import get_db
from backend.app.models.all_models import Movie, Rating, WatchHistory, Genre
from backend.app.schemas.schemas import MovieBase, RatingCreate, RatingResponse, HistoryResponse
from backend.app.routers.auth import get_current_user, User
from backend.ml.engine import engine as recommender

router = APIRouter()

# --- Public Movie Routes ---
@router.get("/movies/search", response_model=List[MovieBase])
def search_movies(
    q: str = Query(..., min_length=2), 
    skip: int = 0, 
    limit: int = 20, 
    db: Session = Depends(get_db)
):
    # SQL ILIKE search
    movies = db.query(Movie).filter(Movie.title.ilike(f"%{q}%")).offset(skip).limit(limit).all()
    return movies

@router.get("/movies/trending", response_model=List[MovieBase])
def get_trending(limit: int = 10, db: Session = Depends(get_db)):
    # Simple logic: order by popularity column which is assumed to be updated via daily cron job
    return db.query(Movie).order_by(Movie.popularity.desc()).limit(limit).all()

@router.get("/movies/{movie_id}", response_model=MovieBase)
def get_movie_details(movie_id: int, db: Session = Depends(get_db)):
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie

# --- Protected Interaction Routes ---
@router.post("/ratings", response_model=RatingResponse)
def rate_movie(
    rating: RatingCreate, 
    user: User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    # Check if movie exists
    if not db.query(Movie).filter(Movie.id == rating.movie_id).first():
        raise HTTPException(status_code=404, detail="Movie not found")

    # Upsert rating
    existing_rating = db.query(Rating).filter(
        Rating.user_id == user.id, 
        Rating.movie_id == rating.movie_id
    ).first()

    if existing_rating:
        existing_rating.rating = rating.rating
        db.commit()
        return existing_rating
    
    new_rating = Rating(user_id=user.id, movie_id=rating.movie_id, rating=rating.rating)
    db.add(new_rating)
    
    # Also add to history implicitly
    history_entry = WatchHistory(user_id=user.id, movie_id=rating.movie_id)
    db.add(history_entry)
    
    db.commit()
    db.refresh(new_rating)
    return new_rating

@router.get("/users/me/history", response_model=List[HistoryResponse])
def get_history(
    skip: int = 0, 
    limit: int = 50, 
    user: User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    return db.query(WatchHistory).filter(
        WatchHistory.user_id == user.id
    ).order_by(WatchHistory.watched_at.desc()).offset(skip).limit(limit).all()

# --- Recommendations ---
@router.get("/recommendations", response_model=List[MovieBase])
def get_recommendations(
    limit: int = 10, 
    user: User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    # Call ML Engine
    recommended_ids = recommender.get_recommendations(user.id, db, n=limit)
    
    # Fetch movie objects in ORDER of recommendations
    # SQL IN clause doesn't guarantee order, so we might need to resort in python or use complex SQL
    movies = db.query(Movie).filter(Movie.id.in_(recommended_ids)).all()
    
    # Sort locally to match recommendation order
    movie_map = {m.id: m for m in movies}
    ordered_movies = [movie_map[mid] for mid in recommended_ids if mid in movie_map]
    
    return ordered_movies

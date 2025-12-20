from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

# --- Auth ---
class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
    user_id: Optional[int] = None

# --- Movies ---
class GenreBase(BaseModel):
    id: int
    name: str

class MovieBase(BaseModel):
    id: int
    tmdb_id: int
    title: str
    overview: Optional[str] = None
    poster_path: Optional[str] = None
    vote_average: float
    genres: List[GenreBase] = []

    class Config:
        from_attributes = True

# --- Ratings ---
class RatingCreate(BaseModel):
    movie_id: int
    rating: float # 1-5

class RatingResponse(BaseModel):
    movie_id: int
    rating: float
    created_at: datetime
    
    class Config:
        from_attributes = True

# --- History ---
class HistoryResponse(BaseModel):
    movie: MovieBase
    watched_at: datetime
    
    class Config:
        from_attributes = True

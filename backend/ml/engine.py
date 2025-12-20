import os
import pickle
import pandas as pd
import numpy as np
from sqlalchemy.orm import Session
from sklearn.metrics.pairwise import cosine_similarity
from backend.app.models.all_models import Rating, Movie, Genre

class RecommenderEngine:
    def __init__(self, model_path="model_data.pkl"):
        self.model_path = model_path
        self.user_item_matrix = None
        self.similarity_matrix = None
        self.movie_ids = []
        self._load_model()

    def _load_model(self):
        """Loads trained model artifacts (User-Item Matrix or Similarity Matrix)"""
        # In a real scenario, we load a large pre-computed matrix
        if os.path.exists(self.model_path):
            with open(self.model_path, 'rb') as f:
                data = pickle.load(f)
                self.user_item_matrix = data.get('user_item_matrix')
                self.similarity_matrix = data.get('similarity_matrix') # Item-Item similarity
                self.movie_ids = data.get('movie_ids', [])
        else:
            print("ML WARNING: No model found. Recommendations will be popularity-based only.")

    def get_recommendations(self, user_id: int, db: Session, n: int = 10):
        """
        Hybrid Strategy:
        1. If user has ratings & model exists -> Item-Item Collaborative Filtering.
        2. Else -> Content-based / Trending / Top Rated.
        """
        user_ratings = db.query(Rating).filter(Rating.user_id == user_id).all()
        
        # Cold Start Case 1: System has no model yet
        if self.similarity_matrix is None:
            return self.get_popular_movies(db, n)

        # Cold Start Case 2: User has no ratings
        if not user_ratings:
            return self.get_popular_movies(db, n)
            
        # Strategy: Item-Item CF
        # 1. Get movies user liked (rating > 3.5)
        liked_movies = [r.movie_id for r in user_ratings if r.rating >= 3.5]
        
        if not liked_movies:
             return self.get_popular_movies(db, n)

        # 2. Find similar items based on pre-computed cosine similarity
        scores = {}
        
        # We need to map DB IDs to Matrix Indices
        # Ideally this map is saved with the model. 
        # For simplicity, assuming movie_ids list matches matrix index.
        try:
             # Basic mapping check
            id_to_idx = {mid: idx for idx, mid in enumerate(self.movie_ids)}
            
            for movie_id in liked_movies:
                if movie_id not in id_to_idx: 
                    continue
                
                idx = id_to_idx[movie_id]
                sim_scores = self.similarity_matrix[idx]
                
                # sim_scores is an array of similarities to all other movies
                for other_idx, score in enumerate(sim_scores):
                    other_id = self.movie_ids[other_idx]
                    if other_id in liked_movies: continue # Don't recommend what they already liked
                    
                    scores[other_id] = scores.get(other_id, 0) + score

            # Sort by accumulated score
            recommended_ids = sorted(scores, key=scores.get, reverse=True)[:n]
            
            if not recommended_ids:
                return self.get_popular_movies(db, n)
                
            return recommended_ids
        except Exception as e:
            print(f"ML Error: {e}")
            return self.get_popular_movies(db, n)

    def get_popular_movies(self, db: Session, n: int = 10):
        """Fallback: Return top rated movies from DB"""
        movies = db.query(Movie).order_by(Movie.popularity.desc()).limit(n).all()
        return [m.id for m in movies]

engine = RecommenderEngine()

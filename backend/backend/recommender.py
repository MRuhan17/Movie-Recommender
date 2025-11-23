"""Hybrid Movie Recommender with Sentiment Analysis

Combines collaborative filtering with sentiment scores from TMDB reviews.
"""

import numpy as np
from typing import List, Dict, Optional
from .sentiment import get_sentiment_features


class HybridRecommender:
    """Hybrid recommender: CF + Sentiment analysis."""
    
    def __init__(
        self,
        cf_model=None,
        sentiment_csv_path: str = None,
        sentiment_weight: float = 0.15
    ):
        """Initialize hybrid recommender.
        
        Args:
            cf_model: Trained CF model (SVD from surprise)
            sentiment_csv_path: Path to sentiment scores CSV
            sentiment_weight: Weight for sentiment in blending (0-1)
        """
        self.cf_model = cf_model
        self.sentiment_weight = sentiment_weight
        self.sentiment_features = get_sentiment_features(
            sentiment_csv_path
        )
    
    def predict_single(
        self,
        user_id: int,
        movie_id: int,
        use_sentiment: bool = True
    ) -> float:
        """Predict rating for user-movie pair.
        
        Args:
            user_id: User ID
            movie_id: Movie ID
            use_sentiment: Whether to blend with sentiment
            
        Returns:
            Predicted rating (0-5)
        """
        if not self.cf_model:
            raise ValueError("CF model not initialized")
        
        # Get CF prediction
        cf_pred = self.cf_model.predict(
            user_id, 
            movie_id
        ).est
        
        # Blend with sentiment if available
        if use_sentiment and self.sentiment_features.has_data():
            final_score = self.sentiment_features.adjust_score(
                cf_pred,
                movie_id,
                weight=self.sentiment_weight
            )
            return min(5.0, max(0.0, final_score))
        
        return cf_pred
    
    def recommend_for_user(
        self,
        user_id: int,
        movie_ids: List[int],
        n_recommendations: int = 10,
        use_sentiment: bool = True
    ) -> List[Dict[str, float]]:
        """Get top N recommendations for user.
        
        Args:
            user_id: User ID
            movie_ids: List of candidate movie IDs
            n_recommendations: Number to return
            use_sentiment: Whether to use sentiment blending
            
        Returns:
            List of {movieId, predicted_rating}
        """
        predictions = []
        
        for movie_id in movie_ids:
            score = self.predict_single(
                user_id,
                movie_id,
                use_sentiment=use_sentiment
            )
            predictions.append({
                "movieId": movie_id,
                "predicted_rating": float(score)
            })
        
        # Sort by rating descending
        predictions.sort(
            key=lambda x: x["predicted_rating"],
            reverse=True
        )
        
        return predictions[:n_recommendations]
    
    def get_sentiment_boost(
        self,
        movie_id: int
    ) -> float:
        """Get sentiment score for a movie.
        
        Args:
            movie_id: Movie ID
            
        Returns:
            Sentiment score (0-1)
        """
        return self.sentiment_features.get_sentiment_score(movie_id)

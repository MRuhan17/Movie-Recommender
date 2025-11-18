"""Sentiment Analysis Module

Integrates TMDB review sentiment with collaborative filtering recommendations.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Optional, Dict


class SentimentFeatures:
    """Manages sentiment scores from CSV files."""
    
    def __init__(self, sentiment_csv_path: str = None):
        self.sentiment_dict = {}
        if sentiment_csv_path and Path(sentiment_csv_path).exists():
            try:
                df = pd.read_csv(sentiment_csv_path)
                self.sentiment_dict = dict(zip(
                    df['movieId'].astype(int),
                    df['sentiment_score'].astype(float)
                ))
            except Exception as e:
                print(f"Error loading sentiment: {e}")
    
    def get_sentiment_score(self, movie_id: int) -> float:
        """Get sentiment (0-1 scale), 0.5 if not found."""
        return self.sentiment_dict.get(movie_id, 0.5)
    
    def adjust_score(
        self,
        pred_rating: float,
        movie_id: int,
        weight: float = 0.15
    ) -> float:
        """Blend CF prediction with sentiment score."""
        if not (0 <= weight <= 1):
            weight = 0.15
        sentiment = self.get_sentiment_score(movie_id)
        sentiment_rating = sentiment * 5  # Scale to 0-5
        return pred_rating * (1 - weight) + sentiment_rating * weight
    
    def has_data(self) -> bool:
        """Check if sentiment data loaded."""
        return len(self.sentiment_dict) > 0


_instance: Optional[SentimentFeatures] = None


def get_sentiment_features(
    csv_path: str = None
) -> SentimentFeatures:
    """Get singleton sentiment instance."""
    global _instance
    if _instance is None:
        _instance = SentimentFeatures(csv_path)
    return _instance

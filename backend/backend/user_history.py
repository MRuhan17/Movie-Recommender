"""
Level 1: User Watch History and Personalized Recommendations
Implements user profile tracking and cosine similarity-based recommendations

Built by Ruhulalemeen Mulla
"""

import json
import numpy as np
from datetime import datetime
from typing import List, Dict, Optional
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import sqlite3
import os


class UserHistoryManager:
    """Manages user watch history and liked movies"""
    
    def __init__(self, db_path: str = "user_history.db"):
        self.db_path = db_path
        self._initialize_database()
    
    def _initialize_database(self):
        """Create database tables if they don't exist"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # User watch history table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS watch_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                movie_id INTEGER NOT NULL,
                movie_title TEXT,
                genres TEXT,
                rating REAL,
                watched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # User likes/favorites table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_likes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                movie_id INTEGER NOT NULL,
                movie_title TEXT,
                genres TEXT,
                liked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(user_id, movie_id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_to_history(self, user_id: str, movie_id: int, movie_title: str, 
                       genres: List[str], rating: float = None):
        """Add a movie to user's watch history"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        genres_str = json.dumps(genres)
        cursor.execute('''
            INSERT INTO watch_history (user_id, movie_id, movie_title, genres, rating)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, movie_id, movie_title, genres_str, rating))
        
        conn.commit()
        conn.close()
    
    def add_like(self, user_id: str, movie_id: int, movie_title: str, genres: List[str]):
        """Add a movie to user's liked movies"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        genres_str = json.dumps(genres)
        try:
            cursor.execute('''
                INSERT INTO user_likes (user_id, movie_id, movie_title, genres)
                VALUES (?, ?, ?, ?)
            ''', (user_id, movie_id, movie_title, genres_str))
            conn.commit()
        except sqlite3.IntegrityError:
            pass  # Already liked
        finally:
            conn.close()
    
    def remove_like(self, user_id: str, movie_id: int):
        """Remove a movie from user's liked movies"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            DELETE FROM user_likes WHERE user_id = ? AND movie_id = ?
        ''', (user_id, movie_id))
        
        conn.commit()
        conn.close()
    
    def get_watch_history(self, user_id: str, limit: int = 50) -> List[Dict]:
        """Get user's watch history"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT movie_id, movie_title, genres, rating, watched_at
            FROM watch_history
            WHERE user_id = ?
            ORDER BY watched_at DESC
            LIMIT ?
        ''', (user_id, limit))
        
        history = []
        for row in cursor.fetchall():
            history.append({
                'movie_id': row[0],
                'title': row[1],
                'genres': json.loads(row[2]),
                'rating': row[3],
                'watched_at': row[4]
            })
        
        conn.close()
        return history
    
    def get_liked_movies(self, user_id: str) -> List[Dict]:
        """Get user's liked movies"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT movie_id, movie_title, genres, liked_at
            FROM user_likes
            WHERE user_id = ?
            ORDER BY liked_at DESC
        ''', (user_id,))
        
        likes = []
        for row in cursor.fetchall():
            likes.append({
                'movie_id': row[0],
                'title': row[1],
                'genres': json.loads(row[2]),
                'liked_at': row[3]
            })
        
        conn.close()
        return likes
    
    def get_user_profile(self, user_id: str) -> Dict:
        """Get comprehensive user profile"""
        return {
            'user_id': user_id,
            'watch_history': self.get_watch_history(user_id),
            'liked_movies': self.get_liked_movies(user_id),
            'total_watched': self._get_watch_count(user_id),
            'total_liked': self._get_like_count(user_id)
        }
    
    def _get_watch_count(self, user_id: str) -> int:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM watch_history WHERE user_id = ?', (user_id,))
        count = cursor.fetchone()[0]
        conn.close()
        return count
    
    def _get_like_count(self, user_id: str) -> int:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM user_likes WHERE user_id = ?', (user_id,))
        count = cursor.fetchone()[0]
        conn.close()
        return count


class PersonalizedRecommender:
    """Generates personalized recommendations using cosine similarity"""
    
    def __init__(self, history_manager: UserHistoryManager):
        self.history_manager = history_manager
        self.vectorizer = TfidfVectorizer()
    
    def get_recommendations(self, user_id: str, candidate_movies: List[Dict], 
                           top_n: int = 10) -> List[Dict]:
        """
        Generate personalized recommendations based on user history
        
        Args:
            user_id: User identifier
            candidate_movies: List of movies to rank (each with id, title, genres, overview)
            top_n: Number of recommendations to return
        
        Returns:
            List of recommended movies with similarity scores
        """
        # Get user profile
        liked_movies = self.history_manager.get_liked_movies(user_id)
        watch_history = self.history_manager.get_watch_history(user_id, limit=20)
        
        if not liked_movies and not watch_history:
            # New user - return popular movies
            return candidate_movies[:top_n]
        
        # Build user taste profile from liked movies and watch history
        user_profile = self._build_user_profile(liked_movies, watch_history)
        
        # Calculate similarity scores
        recommendations = []
        for movie in candidate_movies:
            # Skip if already watched or liked
            movie_id = movie.get('id')
            if self._is_already_interacted(user_id, movie_id):
                continue
            
            similarity = self._calculate_similarity(user_profile, movie)
            recommendations.append({
                **movie,
                'similarity_score': similarity,
                'recommendation_reason': self._get_reason(user_profile, movie)
            })
        
        # Sort by similarity score
        recommendations.sort(key=lambda x: x['similarity_score'], reverse=True)
        
        return recommendations[:top_n]
    
    def _build_user_profile(self, liked_movies: List[Dict], 
                           watch_history: List[Dict]) -> Dict:
        """Build user taste profile from interactions"""
        all_genres = []
        favorite_genres = {}
        
        # Weight liked movies more heavily
        for movie in liked_movies:
            for genre in movie['genres']:
                all_genres.append(genre)
                favorite_genres[genre] = favorite_genres.get(genre, 0) + 2
        
        # Add watch history with lower weight
        for movie in watch_history:
            for genre in movie['genres']:
                all_genres.append(genre)
                favorite_genres[genre] = favorite_genres.get(genre, 0) + 1
        
        # Get top genres
        sorted_genres = sorted(favorite_genres.items(), key=lambda x: x[1], reverse=True)
        top_genres = [g[0] for g in sorted_genres[:5]]
        
        return {
            'all_genres': all_genres,
            'favorite_genres': top_genres,
            'genre_weights': favorite_genres,
            'liked_count': len(liked_movies),
            'watched_count': len(watch_history)
        }
    
    def _calculate_similarity(self, user_profile: Dict, movie: Dict) -> float:
        """Calculate cosine similarity between user profile and movie"""
        # Genre-based similarity
        movie_genres = set(movie.get('genres', []))
        user_genres = set(user_profile['favorite_genres'])
        
        if not user_genres:
            return 0.0
        
        # Jaccard similarity for genres
        genre_intersection = len(movie_genres & user_genres)
        genre_union = len(movie_genres | user_genres)
        genre_similarity = genre_intersection / genre_union if genre_union > 0 else 0.0
        
        # Weight by user's genre preferences
        genre_weight_score = sum(
            user_profile['genre_weights'].get(g, 0) 
            for g in movie_genres
        ) / max(user_profile['genre_weights'].values()) if user_profile['genre_weights'] else 0.0
        
        # Combine scores
        final_score = (genre_similarity * 0.6) + (genre_weight_score * 0.4)
        
        return round(final_score, 4)
    
    def _is_already_interacted(self, user_id: str, movie_id: int) -> bool:
        """Check if user has already watched or liked this movie"""
        liked = self.history_manager.get_liked_movies(user_id)
        watched = self.history_manager.get_watch_history(user_id)
        
        liked_ids = {m['movie_id'] for m in liked}
        watched_ids = {m['movie_id'] for m in watched}
        
        return movie_id in liked_ids or movie_id in watched_ids
    
    def _get_reason(self, user_profile: Dict, movie: Dict) -> str:
        """Generate recommendation reason (preview for Level 3)"""
        matching_genres = set(movie.get('genres', [])) & set(user_profile['favorite_genres'])
        
        if matching_genres:
            genre_list = ', '.join(list(matching_genres)[:2])
            return f"Matches your interest in {genre_list}"
        
        return "Based on your viewing history"


# FastAPI integration example
if __name__ == "__main__":
    # Initialize
    history_manager = UserHistoryManager()
    recommender = PersonalizedRecommender(history_manager)
    
    # Example usage
    user_id = "user_123"
    
    # Add some history
    history_manager.add_like(user_id, 550, "Inception", ["Action", "Sci-Fi", "Thriller"])
    history_manager.add_to_history(user_id, 27205, "Inception", ["Action", "Sci-Fi"], 9.5)
    
    # Get recommendations
    candidate_movies = [
        {'id': 155, 'title': 'The Dark Knight', 'genres': ['Action', 'Crime', 'Drama']},
        {'id': 13, 'title': 'Forrest Gump', 'genres': ['Comedy', 'Drama', 'Romance']},
        {'id': 680, 'title': 'Pulp Fiction', 'genres': ['Thriller', 'Crime']}
    ]
    
    recommendations = recommender.get_recommendations(user_id, candidate_movies)
    print(f"\nTop recommendations for {user_id}:")
    for rec in recommendations:
        print(f"- {rec['title']} (Score: {rec['similarity_score']})")
        print(f"  Reason: {rec['recommendation_reason']}\n")

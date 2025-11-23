"""
Level 2: TMDB API Fusion with ML Recommender
Fetches real movie metadata and fuses with recommendation algorithm

Built by Ruhulalemeen Mulla
"""

import requests
import os
from typing import List, Dict, Optional
from functools import lru_cache
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TMDBFusion:
    """Integrates TMDB API with recommendation system"""
    
    BASE_URL = "https://api.themoviedb.org/3"
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("TMDB_API_KEY")
        if not self.api_key:
            raise ValueError("TMDB API key required")
    
    @lru_cache(maxsize=1000)
    def get_movie_details(self, movie_id: int) -> Optional[Dict]:
        """Fetch comprehensive movie details from TMDB"""
        try:
            response = requests.get(
                f"{self.BASE_URL}/movie/{movie_id}",
                params={"api_key": self.api_key}
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error fetching movie {movie_id}: {e}")
            return None
    
    @lru_cache(maxsize=500)
    def get_movie_credits(self, movie_id: int) -> Optional[Dict]:
        """Fetch cast and crew information"""
        try:
            response = requests.get(
                f"{self.BASE_URL}/movie/{movie_id}/credits",
                params={"api_key": self.api_key}
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error fetching credits for {movie_id}: {e}")
            return None
    
    def enrich_movie_data(self, movie_basic: Dict) -> Dict:
        """
        Enrich basic movie data with TMDB metadata
        
        Args:
            movie_basic: Basic movie dict with at least {id, title}
        
        Returns:
            Enhanced movie dict with TMDB data
        """
        movie_id = movie_basic.get('id')
        if not movie_id:
            return movie_basic
        
        # Get detailed info
        details = self.get_movie_details(movie_id)
        if not details:
            return movie_basic
        
        # Get credits
        credits = self.get_movie_credits(movie_id)
        
        # Build enriched data
        enriched = {
            **movie_basic,
            'tmdb_data': {
                'overview': details.get('overview', ''),
                'release_date': details.get('release_date', ''),
                'runtime': details.get('runtime'),
                'vote_average': details.get('vote_average', 0),
                'vote_count': details.get('vote_count', 0),
                'popularity': details.get('popularity', 0),
                'budget': details.get('budget', 0),
                'revenue': details.get('revenue', 0),
                'tagline': details.get('tagline', ''),
                'poster_path': details.get('poster_path'),
                'backdrop_path': details.get('backdrop_path'),
            }
        }
        
        # Add genres
        if 'genres' in details:
            enriched['genres'] = [g['name'] for g in details['genres']]
        
        # Add director and top cast
        if credits:
            crew = credits.get('crew', [])
            directors = [c['name'] for c in crew if c.get('job') == 'Director']
            enriched['tmdb_data']['director'] = directors[0] if directors else None
            
            cast = credits.get('cast', [])[:5]  # Top 5 actors
            enriched['tmdb_data']['cast'] = [c['name'] for c in cast]
        
        return enriched
    
    def search_movies(self, query: str, page: int = 1) -> List[Dict]:
        """Search movies by query"""
        try:
            response = requests.get(
                f"{self.BASE_URL}/search/movie",
                params={
                    "api_key": self.api_key,
                    "query": query,
                    "page": page
                }
            )
            response.raise_for_status()
            results = response.json().get('results', [])
            return [self.enrich_movie_data(m) for m in results]
        except Exception as e:
            logger.error(f"Error searching movies: {e}")
            return []


class HybridRecommender:
    """Hybrid recommender combining ML model with TMDB data"""
    
    def __init__(self, tmdb_fusion: TMDBFusion, ml_recommender):
        self.tmdb = tmdb_fusion
        self.ml_recommender = ml_recommender
    
    def get_smart_recommendations(self, user_id: str, query: Optional[str] = None,
                                 top_n: int = 10) -> List[Dict]:
        """
        Generate recommendations using both ML model and TMDB data
        
        Args:
            user_id: User identifier
            query: Optional search query for filtering
            top_n: Number of recommendations
        
        Returns:
            Enriched recommendations with TMDB metadata
        """
        # Get candidate movies (from search or trending)
        if query:
            candidates = self.tmdb.search_movies(query)
        else:
            candidates = self._get_trending_movies()
        
        # Get ML-based recommendations
        ml_recommendations = self.ml_recommender.get_recommendations(
            user_id, candidates, top_n=top_n * 2  # Get more for filtering
        )
        
        # Enrich with TMDB data
        enriched_recs = []
        for rec in ml_recommendations[:top_n]:
            enriched = self.tmdb.enrich_movie_data(rec)
            
            # Calculate enhanced score using TMDB data
            tmdb_score = self._calculate_tmdb_score(enriched)
            ml_score = rec.get('similarity_score', 0)
            
            # Weighted combination
            final_score = (ml_score * 0.7) + (tmdb_score * 0.3)
            
            enriched['final_score'] = round(final_score, 4)
            enriched['ml_score'] = ml_score
            enriched['tmdb_score'] = tmdb_score
            
            enriched_recs.append(enriched)
        
        # Re-sort by final score
        enriched_recs.sort(key=lambda x: x['final_score'], reverse=True)
        
        return enriched_recs
    
    def _get_trending_movies(self, page: int = 1) -> List[Dict]:
        """Fetch trending movies from TMDB"""
        try:
            response = requests.get(
                f"{self.tmdb.BASE_URL}/trending/movie/week",
                params={"api_key": self.tmdb.api_key, "page": page}
            )
            response.raise_for_status()
            return response.json().get('results', [])
        except Exception as e:
            logger.error(f"Error fetching trending: {e}")
            return []
    
    def _calculate_tmdb_score(self, movie: Dict) -> float:
        """Calculate quality score from TMDB metadata"""
        tmdb_data = movie.get('tmdb_data', {})
        
        # Normalize vote average (0-10 to 0-1)
        vote_score = tmdb_data.get('vote_average', 0) / 10
        
        # Normalize popularity (log scale)
        import math
        popularity = tmdb_data.get('popularity', 0)
        pop_score = math.log1p(popularity) / math.log1p(1000)  # Cap at 1000
        
        # Vote count factor (more votes = more reliable)
        vote_count = tmdb_data.get('vote_count', 0)
        reliability = min(vote_count / 1000, 1.0)  # Cap at 1000 votes
        
        # Weighted combination
        tmdb_score = (
            vote_score * 0.6 * reliability +  # Weight good ratings
            pop_score * 0.4  # Consider popularity
        )
        
        return round(tmdb_score, 4)
    
    def get_similar_movies(self, movie_id: int, top_n: int = 10) -> List[Dict]:
        """Get similar movies using TMDB's similarity API"""
        try:
            response = requests.get(
                f"{self.tmdb.BASE_URL}/movie/{movie_id}/similar",
                params={"api_key": self.tmdb.api_key}
            )
            response.raise_for_status()
            similar = response.json().get('results', [])
            
            # Enrich and return
            return [self.tmdb.enrich_movie_data(m) for m in similar[:top_n]]
        except Exception as e:
            logger.error(f"Error fetching similar movies: {e}")
            return []


# Example usage
if __name__ == "__main__":
    from .user_history import UserHistoryManager, PersonalizedRecommender
    
    # Initialize components
    tmdb = TMDBFusion(api_key="your_api_key")
    history_mgr = UserHistoryManager()
    ml_rec = PersonalizedRecommender(history_mgr)
    hybrid = HybridRecommender(tmdb, ml_rec)
    
    # Get smart recommendations
    user_id = "user_123"
    recommendations = hybrid.get_smart_recommendations(user_id, top_n=5)
    
    print("\nSmart Recommendations with TMDB Data:")
    for rec in recommendations:
        print(f"\n{rec['title']}")
        print(f"  Final Score: {rec['final_score']}")
        print(f"  ML Score: {rec['ml_score']}, TMDB Score: {rec['tmdb_score']}")
        tmdb_data = rec.get('tmdb_data', {})
        print(f"  Rating: {tmdb_data.get('vote_average')}/10")
        print(f"  Director: {tmdb_data.get('director')}")
        print(f"  Overview: {tmdb_data.get('overview', '')[:100]}...")

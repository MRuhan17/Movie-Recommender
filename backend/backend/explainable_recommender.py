"""
Level 3: Explainable Recommendations
Provides detailed explanations for why each movie is recommended

Built by Ruhulalemeen Mulla
"""

from typing import List, Dict, Optional, Tuple
from collections import defaultdict
import logging

logger = logging.getLogger(__name__)


class ExplainableRecommender:
    """Generates human-readable explanations for recommendations"""
    
    def __init__(self, history_manager, tmdb_fusion):
        self.history_manager = history_manager
        self.tmdb = tmdb_fusion
    
    def explain_recommendation(self, user_id: str, recommended_movie: Dict) -> Dict:
        """
        Generate comprehensive explanation for a single recommendation
        
        Args:
            user_id: User identifier
            recommended_movie: Movie dict with genres, tmdb_data, etc.
        
        Returns:
            Dict with explanation components
        """
        # Get user's profile
        liked_movies = self.history_manager.get_liked_movies(user_id)
        watch_history = self.history_manager.get_watch_history(user_id, limit=20)
        
        explanation = {
            'movie_title': recommended_movie.get('title'),
            'reasons': [],
            'confidence': 0.0,
            'similar_movies': [],
            'detailed_explanation': ''
        }
        
        # Reason 1: Genre match
        genre_reason = self._analyze_genre_match(
            recommended_movie, liked_movies, watch_history
        )
        if genre_reason:
            explanation['reasons'].append(genre_reason)
        
        # Reason 2: Director/Actor match
        talent_reason = self._analyze_talent_match(
            recommended_movie, liked_movies
        )
        if talent_reason:
            explanation['reasons'].append(talent_reason)
        
        # Reason 3: Similar to liked movies
        similar_reason = self._analyze_similarity(
            recommended_movie, liked_movies
        )
        if similar_reason:
            explanation['reasons'].append(similar_reason)
            explanation['similar_movies'] = similar_reason.get('examples', [])
        
        # Reason 4: Quality indicators
        quality_reason = self._analyze_quality(
            recommended_movie
        )
        if quality_reason:
            explanation['reasons'].append(quality_reason)
        
        # Reason 5: Trending/Popular
        popularity_reason = self._analyze_popularity(
            recommended_movie
        )
        if popularity_reason:
            explanation['reasons'].append(popularity_reason)
        
        # Calculate confidence score
        explanation['confidence'] = self._calculate_confidence(explanation['reasons'])
        
        # Generate human-readable text
        explanation['detailed_explanation'] = self._generate_explanation_text(
            explanation
        )
        
        return explanation
    
    def _analyze_genre_match(self, movie: Dict, liked: List[Dict], 
                            watched: List[Dict]) -> Optional[Dict]:
        """Analyze genre-based recommendation reason"""
        movie_genres = set(movie.get('genres', []))
        
        # Count genre preferences from history
        genre_counts = defaultdict(int)
        for m in liked:
            for g in m.get('genres', []):
                genre_counts[g] += 2  # Weighted
        for m in watched:
            for g in m.get('genres', []):
                genre_counts[g] += 1
        
        matching_genres = movie_genres & set(genre_counts.keys())
        
        if matching_genres:
            top_match = max(matching_genres, key=lambda g: genre_counts[g])
            watch_count = genre_counts[top_match]
            
            return {
                'type': 'genre_match',
                'strength': min(len(matching_genres) / len(movie_genres), 1.0),
                'details': {
                    'matching_genres': list(matching_genres),
                    'top_genre': top_match,
                    'watch_count': watch_count
                },
                'message': f"Recommended because you've enjoyed {watch_count} {top_match} movies"
            }
        return None
    
    def _analyze_talent_match(self, movie: Dict, liked: List[Dict]) -> Optional[Dict]:
        """Analyze director/actor match"""
        tmdb_data = movie.get('tmdb_data', {})
        director = tmdb_data.get('director')
        cast = set(tmdb_data.get('cast', []))
        
        if not director and not cast:
            return None
        
        # Find matching talent from liked movies
        liked_directors = []
        liked_actors = set()
        
        for liked_movie in liked:
            liked_tmdb = liked_movie.get('tmdb_data', {})
            if liked_tmdb.get('director'):
                liked_directors.append(liked_tmdb['director'])
            liked_actors.update(liked_tmdb.get('cast', []))
        
        matching_actors = cast & liked_actors
        director_match = director in liked_directors
        
        if director_match:
            return {
                'type': 'director_match',
                'strength': 0.9,
                'details': {'director': director},
                'message': f"Directed by {director}, whose work you've enjoyed before"
            }
        
        if matching_actors:
            actor = list(matching_actors)[0]
            return {
                'type': 'actor_match',
                'strength': 0.7,
                'details': {'actors': list(matching_actors)},
                'message': f"Features {actor}, who you liked in other movies"
            }
        
        return None
    
    def _analyze_similarity(self, movie: Dict, liked: List[Dict]) -> Optional[Dict]:
        """Find similar movies user has liked"""
        if not liked:
            return None
        
        movie_genres = set(movie.get('genres', []))
        
        # Find most similar liked movie
        similarities = []
        for liked_movie in liked:
            liked_genres = set(liked_movie.get('genres', []))
            if not movie_genres or not liked_genres:
                continue
            
            # Jaccard similarity
            intersection = len(movie_genres & liked_genres)
            union = len(movie_genres | liked_genres)
            similarity = intersection / union if union > 0 else 0
            
            if similarity > 0.3:  # Threshold
                similarities.append({
                    'title': liked_movie.get('title'),
                    'similarity': similarity,
                    'common_genres': list(movie_genres & liked_genres)
                })
        
        if similarities:
            similarities.sort(key=lambda x: x['similarity'], reverse=True)
            top_similar = similarities[0]
            
            return {
                'type': 'similar_to_liked',
                'strength': top_similar['similarity'],
                'details': {
                    'reference_movie': top_similar['title'],
                    'common_genres': top_similar['common_genres']
                },
                'examples': [s['title'] for s in similarities[:3]],
                'message': f"Similar to '{top_similar['title']}' which you liked"
            }
        
        return None
    
    def _analyze_quality(self, movie: Dict) -> Optional[Dict]:
        """Analyze movie quality indicators"""
        tmdb_data = movie.get('tmdb_data', {})
        rating = tmdb_data.get('vote_average', 0)
        vote_count = tmdb_data.get('vote_count', 0)
        
        if rating >= 7.5 and vote_count >= 1000:
            return {
                'type': 'high_quality',
                'strength': min(rating / 10, 1.0),
                'details': {
                    'rating': rating,
                    'vote_count': vote_count
                },
                'message': f"Highly rated ({rating}/10) by {vote_count:,} viewers"
            }
        return None
    
    def _analyze_popularity(self, movie: Dict) -> Optional[Dict]:
        """Analyze popularity/trending status"""
        tmdb_data = movie.get('tmdb_data', {})
        popularity = tmdb_data.get('popularity', 0)
        
        if popularity > 50:  # Threshold for trending
            return {
                'type': 'trending',
                'strength': min(popularity / 100, 1.0),
                'details': {'popularity': popularity},
                'message': "Currently trending and popular"
            }
        return None
    
    def _calculate_confidence(self, reasons: List[Dict]) -> float:
        """Calculate overall confidence score"""
        if not reasons:
            return 0.0
        
        # Weight different reason types
        weights = {
            'genre_match': 0.35,
            'similar_to_liked': 0.30,
            'director_match': 0.20,
            'actor_match': 0.10,
            'high_quality': 0.03,
            'trending': 0.02
        }
        
        total_score = sum(
            r['strength'] * weights.get(r['type'], 0.1)
            for r in reasons
        )
        
        return round(min(total_score, 1.0), 4)
    
    def _generate_explanation_text(self, explanation: Dict) -> str:
        """Generate human-readable explanation"""
        reasons = explanation['reasons']
        
        if not reasons:
            return f"We recommend '{explanation['movie_title']}' based on your viewing history."
        
        # Build explanation
        text = f"Why we recommend '{explanation['movie_title']}':\n\n"
        
        for i, reason in enumerate(reasons, 1):
            text += f"{i}. {reason['message']}\n"
        
        # Add confidence
        confidence_pct = int(explanation['confidence'] * 100)
        text += f"\nConfidence: {confidence_pct}%"
        
        # Add similar movies if available
        if explanation.get('similar_movies'):
            text += f"\n\nYou might also like: {', '.join(explanation['similar_movies'][:3])}"
        
        return text


# Example usage
if __name__ == "__main__":
    from user_history import UserHistoryManager
    from tmdb_recommender import TMDBFusion
    
    # Initialize
    history_mgr = UserHistoryManager()
    tmdb = TMDBFusion(api_key="your_key")
    explainer = ExplainableRecommender(history_mgr, tmdb)
    
    # Example movie
    movie = {
        'id': 155,
        'title': 'The Dark Knight',
        'genres': ['Action', 'Crime', 'Drama'],
        'tmdb_data': {
            'director': 'Christopher Nolan',
            'cast': ['Christian Bale', 'Heath Ledger'],
            'vote_average': 9.0,
            'vote_count': 25000,
            'popularity': 150
        }
    }
    
    user_id = "user_123"
    explanation = explainer.explain_recommendation(user_id, movie)
    
    print(explanation['detailed_explanation'])

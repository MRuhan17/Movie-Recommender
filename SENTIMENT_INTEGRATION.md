# Sentiment Analysis Integration Guide

This document explains how sentiment analysis from TMDB reviews is integrated into the Movie Recommender system.

## Overview

The hybrid recommender system combines **Collaborative Filtering (CF)** predictions with **sentiment analysis** scores to improve recommendation quality. TMDB movie reviews are analyzed for sentiment using DistilBERT, and these scores are blended with CF predictions.

## Architecture

### Components

1. **sentiment.py** - Core sentiment feature management
   - Loads sentiment scores from CSV
   - Provides score retrieval and adjustment methods

2. **recommender.py** - Hybrid recommendation engine
   - Integrates CF model with sentiment features
   - Provides prediction and recommendation methods

3. **sentiment_analysis.ipynb** - Notebook for generating sentiment scores
   - Fetches reviews from TMDB API
   - Runs DistilBERT sentiment analysis
   - Outputs CSV file

## Formula

**Blended Score** = CF_prediction × 0.85 + (sentiment_score × 5) × 0.15

Where:
- CF_prediction: Rating from collaborative filtering (0-5 scale)
- sentiment_score: TMDB review sentiment (0-1 scale, 0.5 = neutral)
- 0.85: Weight given to collaborative filtering
- 0.15: Weight given to sentiment analysis

## Usage

### 1. Generate Sentiment Scores

Run the Jupyter notebook to compute sentiment scores:

```bash
jupyter notebooks/sentiment_analysis.ipynb
```

This generates `models/movie_sentiments.csv` with columns:
- movieId: MovieLens ID
- sentiment_score: 0-1 scale
- num_reviews: Count of TMDB reviews analyzed

### 2. Initialize Recommender

```python
from backend.recommender import HybridRecommender

recommender = HybridRecommender(
    cf_model=your_trained_svd_model,
    sentiment_csv_path='models/movie_sentiments.csv',
    sentiment_weight=0.15  # Adjust weight here
)
```

### 3. Get Predictions

```python
# Single prediction
score = recommender.predict_single(
    user_id=1,
    movie_id=100,
    use_sentiment=True
)

# Top-N recommendations
recs = recommender.recommend_for_user(
    user_id=1,
    movie_ids=[1, 2, 3, 4, 5],
    n_recommendations=3,
    use_sentiment=True
)
```

## Configuration

### Sentiment Weight

Adjust sentiment influence (0-1 scale):
- 0.0: Pure CF (no sentiment)
- 0.15: Default (85% CF, 15% sentiment)
- 0.5: Balanced
- 1.0: Pure sentiment

```python
recommender.sentiment_weight = 0.2  # 80% CF, 20% sentiment
```

## API Integration

Example FastAPI endpoint:

```python
from fastapi import FastAPI
from backend.recommender import HybridRecommender

app = FastAPI()
recommender = HybridRecommender(...)

@app.get("/recommendations/{user_id}")
async def get_recommendations(user_id: int, n: int = 10):
    movie_ids = [1, 2, 3, ...]  # Get candidate movies
    recs = recommender.recommend_for_user(
        user_id=user_id,
        movie_ids=movie_ids,
        n_recommendations=n
    )
    return {"recommendations": recs}
```

## Performance Notes

- **Initialization**: One-time CSV load (~100ms for 1000 movies)
- **Prediction**: O(1) lookup + blending (~1ms per prediction)
- **Top-N**: O(n log n) sorting (~10ms for 1000 movies)

## Future Improvements

1. **Dynamic Sentiment**: Cache and refresh sentiment scores periodically
2. **User Sentiment Profiles**: Track user preferences for sentiment type
3. **Multi-language Support**: Analyze reviews in multiple languages
4. **Aspect-based Sentiment**: Separate sentiment for plot, acting, etc.
5. **A/B Testing**: Compare CF-only vs hybrid performance

## Dependencies

See `requirements.txt` for sentiment-specific packages:
- `transformers>=4.35.0` - DistilBERT model
- `torch>=2.0.0` - PyTorch backend
- `tqdm>=4.66.0` - Progress tracking

# Production Movie Recommender Backend

A fully structured, production-grade FastAPI backend for movie recommendations using Hybrid Machine Learning (Item-Item Collaborative Filtering + Content Fallback).

## 🏗 Architecture

The system follows a **Layered Architecture**:
1.  **API Layer** (`routers/`): Handles HTTP requests, authentication (JWT), and input validation (Pydantic).
2.  **Service Layer** (Implicit in routers for simplicity, or explicit in `services/`): orchestrates logic.
3.  **ML Engine** (`ml/`): Isolated component that loads pre-computed models (pickle) and serves predictions.
4.  **Data Layer** (`models/`): SQLAlchemy ORM models mapping to PostgreSQL.

### ML Strategy: Hybrid Filtering
*   **Collaborative Filtering (CF)**: Uses **Item-Item Cosine Similarity**. We compute a similarity matrix between movies based on user ratings. If User A likes "Inception", and "Inception" is similar to "Interstellar" (because other users rated both high), we recommend "Interstellar".
*   **Cold Start**: If a user has no history or the model isn't trained, we fallback to **Popularity-based** (trending movies).
*   **Offline Training**: `scripts/train_model.py` runs as a background job (cron) to fetch fresh SQL data, retrain the matrix, and save `model_data.pkl`.

## 🗄 SQL Schema & Database

We use **PostgreSQL**.
*   **Users**: Identity & Auth.
*   **Movies**: Metadata cache (Title, Overview, Genres).
*   **Ratings**: Explicit 1-5 feedback. **Constraint**: Unique(user_id, movie_id).
*   **WatchHistory**: Log of watched items (Implicit feedback).
*   **MovieGenres**: Many-to-Many link.

### Optimized SQL Query (Example: Trending)
To get trending movies efficiently:
```sql
SELECT * FROM movies ORDER BY popularity DESC LIMIT 10;
```
*   **Why**: We index the `popularity` column. This simple query avoids complex joins at runtime, as popularity is pre-calculated/updated during data ingestion.

For History:
```sql
SELECT * FROM watch_history WHERE user_id = :uid ORDER BY watched_at DESC;
```
*   **Why**: Index on `(user_id, watched_at)` makes retrieval O(log N) instead of scanning the whole table.

## 🚀 How to Run Locally

### 1. Prerequisites
*   Python 3.10+
*   PostgreSQL running locally (or update .env)

### 2. Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Configure Environment
# Create .env file with:
DATABASE_URL=postgresql://user:password@localhost/movie_db
SECRET_KEY=your_secret
```

### 3. Run Backend
```bash
# From the root directory:
uvicorn backend.app.main:app --reload
```
Access docs at: `http://localhost:8000/docs`

### 4. Train Model
To generate the first model artifact (requires data in DB):
```bash
python -m backend.scripts.train_model
```

# Setup Guide

## Quick Start for Local Development

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Start the Backend

```bash
cd backend
python app.py
```

The backend will start on `http://localhost:8000`

**Note**: The backend includes mock movie data for development when TMDB API key is not configured. The application will work out of the box without requiring any API keys!

### 3. Serve the Frontend

In a new terminal:

```bash
cd frontend
python -m http.server 3000
```

Or use any static file server:
```bash
# Using Node.js http-server
npx http-server frontend -p 3000

# Or using Python 3
cd frontend && python3 -m http.server 3000
```

### 4. Open in Browser

Navigate to: `http://localhost:3000/index.html`

You should now see the movie recommender with 10 classic movies displayed!

## Using with Real TMDB API

To use real movie data from TMDB instead of mock data:

1. Get a free API key from [TMDB](https://www.themoviedb.org/settings/api)

2. Create a `.env` file in the project root:
   ```bash
   cp .env.example .env
   ```

3. Add your API key to `.env`:
   ```
   TMDB_API_KEY=your_actual_api_key_here
   ```

4. Restart the backend

The backend will automatically detect the API key and use real TMDB data!

## Features

- **Trending Movies**: See what's popular right now
- **Top Rated**: Discover critically acclaimed films
- **Recommendations**: Get personalized movie suggestions
- **Search**: Find specific movies (works with real TMDB API)
- **Movie Details**: Click any movie to see full details

## Deployment

The frontend automatically detects whether it's running locally or in production:
- **Local** (`localhost` or `127.0.0.1`): Uses `http://localhost:8000/api`
- **Production**: Uses the configured production API URL

## Troubleshooting

### Backend not starting?
- Make sure all dependencies are installed: `pip install -r requirements.txt`
- Check if port 8000 is available

### Frontend not showing movies?
- Make sure the backend is running on port 8000
- Check browser console for any error messages
- Verify the API URL is correctly set (should auto-detect for localhost)

### Want to use your own backend URL?
Edit `frontend/index.html` and modify the `API_URL` constant.

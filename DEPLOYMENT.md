# Deployment Guide

This guide covers how to deploy the Movie Recommender application on various platforms.

## Prerequisites

Before deploying, make sure you have:
- A TMDB API key from [themoviedb.org](https://www.themoviedb.org/settings/api)
- Git installed
- Python 3.11+ (for local development)

## Environment Variables

Create a `.env` file based on `.env.example` with the following variables:

```bash
TMDB_API_KEY=your_tmdb_api_key_here
SECRET_KEY=your_secret_key_here_min_32_characters
DATABASE_URL=sqlite:///./movie_recommender.db
```

## Local Development

### Using Python directly

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the backend server:
```bash
python main.py
```

3. Open the frontend:
```bash
# Open frontend/index.html in your browser
# Or serve it with a simple HTTP server:
python -m http.server 3000 --directory frontend
```

The backend API will be available at `http://localhost:8000`

### Using Docker Compose

1. Make sure Docker and Docker Compose are installed
2. Set environment variables in `.env`
3. Build and run:

```bash
docker-compose up --build
```

This will start:
- Backend API at `http://localhost:8000`
- Frontend at `http://localhost:3000`

## Deploy to Render (Backend)

1. Fork/clone this repository
2. Create a new Web Service on [Render](https://render.com)
3. Connect your GitHub repository
4. Render will automatically detect `render.yaml`
5. Add environment variable:
   - `TMDB_API_KEY`: Your TMDB API key
6. Deploy!

The backend will be available at: `https://your-app.onrender.com`

## Deploy to Vercel (Frontend)

1. Fork/clone this repository
2. Install Vercel CLI:
```bash
npm i -g vercel
```

3. Deploy:
```bash
vercel
```

4. Follow the prompts to deploy the frontend

Alternatively, you can deploy via the [Vercel Dashboard](https://vercel.com/dashboard):
- Import your GitHub repository
- Vercel will detect the configuration from `vercel.json`
- Deploy!

## Deploy with Docker

### Backend Docker Image

Build the backend image:
```bash
docker build -f backend/Dockerfile -t movie-recommender-backend .
```

Run the backend:
```bash
docker run -p 8000:8000 -e TMDB_API_KEY=your_key movie-recommender-backend
```

### Frontend Docker Image

Build the frontend image:
```bash
docker build -f frontend/Dockerfile -t movie-recommender-frontend frontend/
```

Run the frontend:
```bash
docker run -p 3000:80 movie-recommender-frontend
```

## API Endpoints

Once deployed, your backend will have the following endpoints:

- `GET /` - API status
- `GET /health_check` - Health check endpoint
- `GET /api/movies/trending` - Get trending movies
- `GET /api/movies/search?query={query}` - Search for movies
- `GET /api/recommendations/{user_id}` - Get personalized recommendations
- `GET /api/explain/{user_id}/{movie_id}` - Explain a recommendation
- `POST /api/history/add` - Add movie to user history

## Troubleshooting

### TMDB API Key Issues

If you see "TMDB API key not configured":
1. Make sure your `.env` file has `TMDB_API_KEY`
2. On Render, add it as an environment variable in the dashboard
3. Restart your service

### Docker Build Fails

If Docker build fails with SSL certificate errors:
- This is usually a temporary network issue
- Try building again after a few minutes
- Or build locally and push to a container registry

### Frontend Can't Connect to Backend

1. Update the API URL in `frontend/index.html`:
```javascript
const API_URL = 'https://your-backend.onrender.com/api';
```

2. Make sure CORS is configured correctly in `backend/app.py` (already done)

## Monitoring

- Check backend logs: `docker logs movie-recommender-backend` (Docker) or check Render dashboard
- Test health check: `curl https://your-backend.onrender.com/health_check`

## Updates

To update your deployment:

1. Make changes to your code
2. Commit and push to GitHub
3. Render/Vercel will automatically redeploy (if auto-deploy is enabled)

Or manually redeploy:
```bash
# Render
git push origin main

# Vercel
vercel --prod
```

## Support

For issues or questions, please open an issue on the GitHub repository.

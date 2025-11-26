# 🎬 Movie Recommender Web App (ML + Full Stack) 

![Python](https://img.shields.io/badge/Python-3.11-blue)
![License](https://img.shields.io/badge/License-Apache--2.0-yellow)
![Platform](https://img.shields.io/badge/Platform-GitHub%20Codespaces-lightgrey)
![Deploy](https://github.com/MRuhan17/Movie-Recommender/actions/workflows/deploy.yml/badge.svg)

A full-stack movie recommender system combining Collaborative Filtering (SVD) and Deep Learning embeddings.
Developed in GitHub Codespaces, integrated with the TMDB API for real-world movie metadata.

### 🧠 Features
- Hybrid recommender engine (CF + Deep Embeddings)
- TMDB API for live movie data
- End-to-end ML pipeline: data → model → API → frontend
- Deployable via Docker on Render & Vercel

### ⚙️ Stack
Python • scikit-surprise • FastAPI • Next.js • Tailwind • TMDB API • Render • Vercel

### 🗂️ Structure
```
movie-recommender/
├── backend/
│   ├── __init__.py
│   ├── app.py
│   ├── recommender.py
│   ├── tmdb_utils.py
│   └── database.py
├── data/
│   ├── movies.csv
│   ├── ratings.csv
│   ├── links.csv
│   └── tags.csv
├── models/
│   └── cf_model.pkl
├── notebooks/
│   ├── model_train.ipynb
│   └── tmdb_test.ipynb
├── .gitignore
├── .env
├── LICENSE
├── README.md
└── requirements.txt
```

### 🧩 Setup

```bash
pip install -r requirements.txt
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 🚀 Deployment

This project includes automated deployment via GitHub Actions:

- **Backend**: Automatically deploys to Render when PRs are merged to main
- **Frontend**: Automatically deploys to Vercel when PRs are merged to main

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions and configuration.

### 📝 License
Apache-2.0

### ⚙️ Run in GitHub Codespaces
1. Open the repo → **Code → Open with Codespaces**
2. Wait for the dev container to build
3. Run `pip install -r requirements.txt`
4. Launch Jupyter with `jupyter notebook --ip=0.0.0.0 --port=8888`

### 🎞️ App Preview

**Personalized Movie Recommendations with Modern UI**

The web app features a clean, responsive interface built with Next.js and Tailwind CSS:

- **🎭 Home Dashboard**: Browse trending movies with TMDB posters and ratings
- **🤖 Smart Recommendations**: Get personalized suggestions based on your viewing history
- **🔍 Search & Filter**: Find movies by genre, year, or rating
- **🎨 Movie Cards**: Beautiful cards showing poster, title, rating, and ML confidence score
- **📊 Stats Dashboard**: Visualize your taste profile and model predictions

**Tech Stack UI**:
```
Frontend: Next.js 14 + Tailwind CSS + Framer Motion
Backend API: FastAPI + Uvicorn
ML Engine: Scikit-surprise (CF) + PyTorch (Embeddings)
Data Source: TMDB API (Live movie metadata + posters)
```

*Note: Screenshots coming soon after Week 4 deployment* 🚀

### 🌐 Vercel Deployment
The application is deployed on Vercel. Ensure `TMDB_API_KEY` is set in the project settings for full functionality.

# 🎬 Movie Recommender Web App  
Hybrid ML Recommender System | FastAPI Backend | Next.js Frontend | Deployed on Vercel

![Python](https://img.shields.io/badge/Python-3.11-blue)
![License](https://img.shields.io/badge/License-Apache--2.0-yellow)
![Platform](https://img.shields.io/badge/Codespaces-Ready-lightgrey)
![Deploy](https://github.com/MRuhan17/Movie-Recommender/actions/workflows/deploy.yml/badge.svg)

A production-ready full-stack movie recommendation system built using a hybrid ML engine combining Collaborative Filtering (SVD) and Semantic Embeddings.  
The system retrieves real-time movie metadata using the TMDB API and serves a clean, fast UI through a modern Next.js frontend.

This project demonstrates ML engineering, API design, full-stack development, and deployment automation.

---

# 🔥 Live Demo
Vercel Deployment:  
https://movie-recommender-7yjq9f4rt-mruhan17s-projects.vercel.app/

---

# 🧠 Core Features

Hybrid ML Recommendation Engine  
- SVD-based Collaborative Filtering  
- Sentence-Transformer embedding similarity  
- Weighted hybrid scoring for improved accuracy and diversity  

Real-time Movie Metadata  
- TMDB API for posters, descriptions, genres, and ratings  
- Fallback logic when metadata is missing  

Full-Stack Implementation  
- FastAPI backend  
- Next.js 14 frontend with Tailwind  
- Deployed using Docker, Render, and Vercel  
- Fast, responsive UI

---

# 🧩 Architecture Overview

                     ┌───────────────────────────┐
                     │        Frontend (Next.js) │
                     │  UI, Movie Cards, Routing │
                     └──────────────┬────────────┘
                                    │
                             HTTP (fetch)
                                    │
                 ┌──────────────────▼──────────────────┐
                 │         FastAPI Backend             │
                 │  /recommend, /movie, /search routes │
                 └──────────────┬──────────────────────┘
                                │
   ┌────────────────────────────┼────────────────────────────┐
   │                            │                            │
┌──▼───┐                  ┌─────▼─────┐                ┌─────▼─────┐
│ CF   │                  │ Embedding │                │ TMDB API   │
│ Model│                  │ Model     │                │ Metadata   │
└──────┘                  └───────────┘                └────────────┘
   │                            │                            │
   └─────── Hybrid Fusion Engine ────────────────► Final Movie List

---

# 🗂️ Project Structure

movie-recommender/
│
├── backend/
│   ├── app.py
│   ├── recommender.py
│   ├── tmdb_utils.py
│   └── database.py
│
├── frontend/
│   ├── app/
│   └── components/
│
├── models/
│   └── cf_model.pkl
│
├── data/
│   ├── movies.csv
│   ├── ratings.csv
│   ├── links.csv
│   └── tags.csv
│
├── notebooks/
│   ├── model_train.ipynb
│   └── tmdb_test.ipynb
│
├── DEPLOYMENT.md
├── LICENSE
└── requirements.txt

---

# ⚙️ Technology Stack

Backend  
- Python 3.11  
- FastAPI + Uvicorn  
- Scikit-Surprise (SVD)  
- Sentence-Transformers  
- TMDB API  
- Pydantic  

Frontend  
- Next.js 14  
- Tailwind CSS  
- Framer Motion  
- Fully responsive components  

Deployment & Infra  
- Vercel (Frontend)  
- Render / Docker (Backend)  
- GitHub Actions CI  
- GitHub Codespaces  

---

# 🧬 Machine Learning Logic

Collaborative Filtering (CF)  
- SVD model trained on MovieLens dataset  
- Learns user–item preference matrix  
- Ideal for preference prediction  

Embedding Similarity  
- Sentence-Transformer embeddings  
- Cosine similarity scores  
- Helps when CF has sparse data  

Hybrid Fusion  
final_score = 0.6 * CF_score + 0.4 * Embedding_score

---

# 🚀 Running Locally

Backend  
1. cd backend  
2. python -m venv venv  
3. source venv/bin/activate   (Windows: venv\Scripts\activate)  
4. pip install -r requirements.txt  
5. uvicorn app:app --reload  

Frontend  
1. cd frontend  
2. npm install  
3. npm run dev  

Environment Variables  
Create `.env`:


---

# 🔄 Deployment Pipeline (CI/CD)

- GitHub Actions runs builds and project checks on each push  
- Frontend auto-deploys to Vercel  
- Backend deploys via Docker (Render)  
- Ensures reproducible builds and stable releases  

---

# 🎨 UI Preview

The app includes:  
- Clean, modern UI  
- Movie cards with posters, ratings, and genres  
- Real-time recommendations  
- Smooth animations via Framer Motion  
- Fully mobile-responsive design  



---

# 📜 License
Apache 2.0

---

# 📡 Production Deployment
The application is deployed on Vercel.  
TMDB_API_KEY is configured in Vercel Environment Variables.

# 🎬 Movie Recommender Web App  
Hybrid ML Recommender System | FastAPI Backend | Next.js Frontend | Deployed on Vercel

![Python](https://img.shields.io/badge/Python-3.11-blue)
![License](https://img.shields.io/badge/License-Apache--2.0-yellow)
![Platform](https://img.shields.io/badge/Codespaces-Ready-lightgrey)

A production-ready full-stack movie recommendation system built using a hybrid ML engine combining Collaborative Filtering (SVD) and Semantic Embeddings.  
The system retrieves real-time movie metadata using the TMDB API and serves a clean, fast UI through a modern Next.js frontend.

---

# 🔥 Live Demo
Vercel Deployment:  
https://movie-recommender-7yjq9f4rt-mruhan17s-projects.vercel.app/

---

# 🧠 Core Features
- Hybrid ML engine (SVD CF + Sentence-Transformers Embeddings)  
- Real-time movie metadata via TMDB API  
- Clean FastAPI backend architecture  
- Modern Next.js 14 frontend with Tailwind  
- Fully responsive UI with smooth animations  

---

# 🧩 Architecture Overview

```
                     ┌───────────────────────────┐
                     │        Frontend (Next.js) │
                     │     UI, Movie Cards, UX   │
                     └──────────────┬────────────┘
                                    │
                             HTTP Requests
                                    │
                 ┌──────────────────▼──────────────────┐
                 │            FastAPI Backend          │
                 │   /recommend   /movie   /search     │
                 └──────────────┬──────────────────────┘
                                │
   ┌────────────────────────────┼────────────────────────────┐
   │                            │                            │
┌──▼────────┐             ┌─────▼────────┐            ┌──────▼─────┐
│ CF Model  │             │ Embedding    │            │ TMDB API    │
│  (SVD)    │             │ Model (ST)   │            │  Metadata   │
└───────────┘             └──────────────┘            └─────────────┘
       │                         │                           │
       └───────────── Hybrid Fusion Engine ───────────────► Final Movie List
```

---

# 🗂️ Project Structure

```
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
```

---

# ⚙️ Technology Stack

### Backend
- Python 3.11  
- FastAPI + Uvicorn  
- Scikit-Surprise (SVD)  
- Sentence-Transformers  
- TMDB API  
- Pydantic  

### Frontend
- Next.js 14  
- Tailwind CSS  
- Framer Motion  
- Responsive and fast movie browsing UI  

### Deployment & Infra
- Vercel (Frontend)  
- Docker + Render (Backend)  
- GitHub Codespaces  
- Clean project structure for portability  

---

# 🧬 Machine Learning Logic

### Collaborative Filtering (CF)
- SVD model trained on MovieLens dataset  
- Learns latent user–item preference patterns  

### Embedding Similarity
- Sentence-Transformer embeddings  
- Cosine similarity for semantic closeness  

### Hybrid Fusion
```
final_score = 0.6 * CF_score + 0.4 * Embedding_score
```

---

# 🚀 Running Locally

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

### Environment Variables
Create `.env`:

```
TMDB_API_KEY=your_key_here
```

---

# 🔄 Deployment Pipeline
- GitHub Actions performs project checks  
- Frontend automatically deploys to Vercel  
- Backend deploys via Docker (Render)  
- Ensures consistent, reproducible releases  

---

# 🎨 UI Preview
The UI includes:
- Clean, modern layout  
- Movie cards with poster, rating, genres  
- Instant recommendations  
- Smooth animations using Framer Motion  
- Mobile-responsive design  

(Add screenshots here if needed.)

---

# 📜 License
Apache 2.0

---

# 📡 Production Deployment
The application is deployed on **Vercel**.  
TMDB_API_KEY is configured in Vercel Project Settings.

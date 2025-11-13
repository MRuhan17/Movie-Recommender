# 🎬 Movie Recommender Web App (ML + Full Stack)

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

### 📝 License
Apache-2.0
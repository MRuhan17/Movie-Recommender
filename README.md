# 🎬 Movie Recommender Web App (ML + Full Stack)

![Python](https://img.shields.io/badge/Python-3.11-blue)
![License](https://img.shields.io/badge/License-Apache--2.0-yellow)
![Platform](https://img.shields.io/badge/Platform-GitHub%20Codespaces-lightgrey)

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

### ⚙️ Run in GitHub Codespaces
1. Open the repo → **Code → Open with Codespaces**
2. Wait for the dev container to build
3. Run `pip install -r requirements.txt`
4. Launch Jupyter with `jupyter notebook --ip=0.0.0.0 --port=8888`

### 📊 Example Recommendation Output

```json
{
  "user_id": 42,
  "recommendations": [
    {"movie_id": 50, "predicted_rating": 4.23, "title": "The Usual Suspects"},
    {"movie_id": 318, "predicted_rating": 4.18, "title": "Shawshank Redemption"},
    {"movie_id": 527, "predicted_rating": 4.15, "title": "Schindler's List"}
  ]
}
```
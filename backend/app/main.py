from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.routers import auth, movies
from backend.app.database import engine, Base

# Create tables if not exist (Simulating migration for simple setup)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Pro Movie Recommender", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(movies.router, prefix="/api", tags=["Movies"])

@app.get("/")
def root():
    return {"message": "Service is live. Visit /docs for Swagger UI"}

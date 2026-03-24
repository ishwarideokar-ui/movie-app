from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd

from backend.auth import router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load movies safely
try:
    movies = pd.read_csv("data/movies.csv")
    print("Movies loaded ✅")
except:
    movies = None
    print("movies.csv NOT FOUND ❌")

app.include_router(router)

@app.get("/")
def home():
    return {"message": "App running 🚀"}

@app.get("/movies")
def get_movies():
    if movies is None:
        return {"message": "No movies file"}
    # Add full poster URL
    movies_copy = movies.copy()
    movies_copy['poster'] = "https://image.tmdb.org/t/p/w500" + movies_copy['poster']
    return movies_copy.head(20).to_dict(orient="records")

@app.get("/recommend")
def recommend(movie: str = ""):
    if movies is None:
        return {"message": "No movies file"}

    if movie.strip() == "":
        return {"message": "Enter movie"}

    result = movies[movies["title"].str.lower().str.contains(movie.lower())]

    if result.empty:
        return {"message": "No movie found"}

    # Add full poster URL
    result_copy = result.copy()
    result_copy['poster'] = "https://image.tmdb.org/t/p/w500" + result_copy['poster']
    return result_copy.head(10).to_dict(orient="records")
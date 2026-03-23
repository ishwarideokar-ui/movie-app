from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import requests

from backend.auth import router
from backend.database import SessionLocal, User

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# TMDB API Key
API_KEY = "533d900aa6f08eb65ad4bcbc91bd71d3"

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
    return movies_copy.head(50).to_dict(orient="records")

@app.get("/movie/{movie_id}")
def get_movie_details(movie_id: int):
    if movies is None:
        return {"message": "No movies file"}

    movie = movies[movies["id"] == movie_id]
    if movie.empty:
        return {"message": "Movie not found"}

    movie_data = movie.iloc[0].to_dict()
    movie_data['poster'] = "https://image.tmdb.org/t/p/w500" + movie_data['poster']

    # Fetch additional details from TMDB
    try:
        # Get movie details
        details_url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}"
        details_response = requests.get(details_url, timeout=10)
        if details_response.status_code == 200:
            details = details_response.json()
            movie_data.update({
                'runtime': details.get('runtime'),
                'release_date': details.get('release_date'),
                'genres': [g['name'] for g in details.get('genres', [])]
            })

        # Get cast
        cast_url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key={API_KEY}"
        cast_response = requests.get(cast_url, timeout=10)
        if cast_response.status_code == 200:
            cast_data = cast_response.json()
            movie_data['cast'] = cast_data.get('cast', [])[:10]  # Top 10 cast

        # Get trailer
        video_url = f"https://api.themoviedb.org/3/movie/{movie_id}/videos?api_key={API_KEY}"
        video_response = requests.get(video_url, timeout=10)
        if video_response.status_code == 200:
            video_data = video_response.json()
            videos = video_data.get('results', [])
            # prioritize official trailers
            trailer = next((v for v in videos if v['site'] == 'YouTube' and v['type'] == 'Trailer' and v.get('official')), None)
            if not trailer:
                trailer = next((v for v in videos if v['site'] == 'YouTube' and v['type'] == 'Trailer'), None)
            if not trailer:
                trailer = next((v for v in videos if v['site'] == 'YouTube'), None)
            if trailer and trailer.get('key'):
                key = trailer['key']
                # Use privacy-enhanced endpoint and origin parameter for safer playback
                movie_data['trailer'] = f"https://www.youtube-nocookie.com/embed/{key}?rel=0&modestbranding=1"
                movie_data['watch_url'] = f"https://www.youtube.com/watch?v={key}"
                movie_data['trailer_name'] = trailer.get('name')

        # Get similar movies
        similar_url = f"https://api.themoviedb.org/3/movie/{movie_id}/similar?api_key={API_KEY}&page=1"
        similar_response = requests.get(similar_url, timeout=10)
        if similar_response.status_code == 200:
            similar_data = similar_response.json()
            similar_movies = similar_data.get('results', [])[:6]  # Top 6
            for sm in similar_movies:
                sm['poster_path'] = "https://image.tmdb.org/t/p/w500" + sm.get('poster_path', '') if sm.get('poster_path') else ''
            movie_data['similar'] = similar_movies

    except Exception as e:
        print(f"Error fetching details: {e}")

    return movie_data

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


# ============== ADMIN ENDPOINTS ==============

@app.get("/admin/users")
def get_all_users():
    db = SessionLocal()
    try:
        users = db.query(User).all()
        return [{"id": u.id, "username": u.username, "is_admin": u.is_admin} for u in users]
    finally:
        db.close()


@app.delete("/admin/users/{user_id}")
def delete_user(user_id: int):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return {"success": False, "message": "User not found"}
        db.delete(user)
        db.commit()
        return {"success": True, "message": "User deleted successfully"}
    except Exception as e:
        db.rollback()
        return {"success": False, "message": f"Error: {str(e)}"}
    finally:
        db.close()


@app.post("/admin/users/{user_id}/make-admin")
def make_user_admin(user_id: int):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return {"success": False, "message": "User not found"}
        user.is_admin = 1
        db.commit()
        return {"success": True, "message": "User is now an admin"}
    except Exception as e:
        db.rollback()
        return {"success": False, "message": f"Error: {str(e)}"}
    finally:
        db.close()


@app.post("/admin/users/{user_id}/remove-admin")
def remove_user_admin(user_id: int):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return {"success": False, "message": "User not found"}
        user.is_admin = 0
        db.commit()
        return {"success": True, "message": "Admin privileges removed"}
    except Exception as e:
        db.rollback()
        return {"success": False, "message": f"Error: {str(e)}"}
    finally:
        db.close()


@app.get("/admin/stats")
def get_admin_stats():
    db = SessionLocal()
    try:
        total_users = db.query(User).count()
        admin_users = db.query(User).filter(User.is_admin == 1).count()
        regular_users = total_users - admin_users
        total_movies = len(movies) if movies is not None else 0
        
        return {
            "total_users": total_users,
            "admin_users": admin_users,
            "regular_users": regular_users,
            "total_movies": total_movies
        }
    except Exception as e:
        return {"error": str(e)}
    finally:
        db.close()
from fastapi import APIRouter
from pydantic import BaseModel
from backend.database import SessionLocal, User

router = APIRouter()

class UserCreate(BaseModel):
    username: str
    password: str

@router.post("/signup")
def signup(user: UserCreate):
    db = SessionLocal()
    try:
        new_user = User(
            username=user.username,
            password=user.password
        )
        db.add(new_user)
        db.commit()
        return {"success": True, "message": "signup successful"}
    except Exception as e:
        db.rollback()
        return {"success": False, "message": f"Error: {str(e)}"}
    finally:
        db.close()

@router.post("/login")
def login(user: UserCreate):
    db = SessionLocal()
    try:
        found = db.query(User).filter(
            User.username == user.username,
            User.password == user.password
        ).first()

        if found:
            return {
                "success": True,
                "message": "Login successful",
                "is_admin": found.is_admin
            }
        else:
            return {"success": False, "message": "Invalid credentials"}
    except Exception as e:
        return {"success": False, "message": f"Error: {str(e)}"}
    finally:
        db.close()
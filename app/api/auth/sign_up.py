from datetime import timedelta

from fastapi import APIRouter, HTTPException

from app.core.database import get_database_connection
from app.core.security import get_password_hash, create_access_token, authenticate_user
from app.api.auth.schemas import User
from dotenv import load_dotenv
import os

SECRET_KEY = os.getenv("SECRET_KEY")

# Hash algorithm for password hashing
HASH_ALGORITHM = os.getenv("HASH_ALGORITHM", "bcrypt")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 1440)

router = APIRouter()


@router.post("/signup")
def signup(user: User):
    client = get_database_connection()
    db = client["CometLabs"]  # Replace "CometLabs" with your actual database name
    collection = db["users"]
    user_exists = collection.find_one({"email": user.email})

    if user_exists:
        raise HTTPException(status_code=400, detail="User already exists")

    hashed_password = get_password_hash(user.password)
    user.password = hashed_password

    collection.insert_one(user.dict())

    access_token = create_access_token(
        data={"sub": user.email, "role": user.role},
        expires_delta=timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES)),
    )

    return {"email": user.email, "access_token": access_token}
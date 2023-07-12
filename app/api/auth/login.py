from datetime import timedelta
from typing import Dict

from fastapi import APIRouter, HTTPException

from core.database import get_database_connection
from core.security import get_password_hash, create_access_token, authenticate_user
from api.auth.schemas import User, LoginData
from dotenv import load_dotenv
import os



load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")

# Hash algorithm for password hashing
HASH_ALGORITHM = os.getenv("HASH_ALGORITHM", "bcrypt")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 1440)

router = APIRouter()


# Login endpoint


@router.post("/login")
def login(data: LoginData):
    authenticated_user = authenticate_user(data.email, data.password)
    if not authenticated_user:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    access_token = create_access_token(
        data={"sub": authenticated_user.email, "role": authenticated_user.role},
        expires_delta=timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES)),
    )

    return {"email": authenticated_user.email, "access_token": access_token}

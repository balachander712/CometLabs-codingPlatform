from datetime import datetime, timedelta

from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from passlib.hash import bcrypt
import jwt
from jwt.exceptions import InvalidTokenError
from dotenv import load_dotenv
import os

from api.auth.schemas import User
from core.database import get_database_connection

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")

HASH_ALGORITHM = os.getenv("HASH_ALGORITHM", "bcrypt")
security = HTTPBearer()


def get_password_hash(password):
    return bcrypt.hash(password)


async def validate_admin_roles(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[HASH_ALGORITHM])
        role = payload.get("role")
        if role != "admin":
            raise HTTPException(status_code=403, detail="Insufficient permissions")
    except InvalidTokenError:
        raise HTTPException(status_code=403, detail="Invalid token")


async def validate_user_roles(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[HASH_ALGORITHM])
        role = payload.get("role")
        if role != "user":
            raise HTTPException(status_code=403, detail="Insufficient permissions")
    except InvalidTokenError:
        raise HTTPException(status_code=403, detail="Invalid token")


def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")
    return encoded_jwt


def verify_password(plain_password, hashed_password):
    return bcrypt.verify(plain_password, hashed_password)


def authenticate_user(email: str, password: str):
    client = get_database_connection()
    db = client["CometLabs"]  # Replace "CometLabs" with your actual database name
    collection = db["users"]
    user_data = collection.find_one({"email": email})
    if not user_data:
        raise HTTPException(status_code=400, detail="User does not exist, Sign Up First")
    if not verify_password(password, user_data["password"]):
        raise HTTPException(status_code=401, detail="Invalid Password")

    user = User(**user_data)
    return user

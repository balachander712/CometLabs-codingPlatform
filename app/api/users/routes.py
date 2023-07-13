from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials
import jwt
from jwt.exceptions import InvalidTokenError

from core.security import validate_admin_roles, security

from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

router = APIRouter()

SECRET_KEY = os.getenv("SECRET_KEY")

# Hash algorithm for password hashing
HASH_ALGORITHM = os.getenv("HASH_ALGORITHM", "bcrypt")

@router.get("/admin-only")
async def admin_only_route(credentials: HTTPAuthorizationCredentials = Depends(security)):
    await validate_admin_roles(credentials)
    return {"message": "You are an admin and have access to this route"}


# Example route accessible by participants and admins
@router.get("/public-route")
async def public_route(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(
            credentials.credentials, SECRET_KEY, algorithms=[HASH_ALGORITHM]
        )
        role = payload.get("role")
        return {"message": f"You are a {role} and have access to this route"}
    except InvalidTokenError:
        raise HTTPException(status_code=403, detail="Invalid token")

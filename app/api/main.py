from fastapi import FastAPI
from api.auth.routes import router as auth_router
from api.users.routes import router as users_router

app = FastAPI()

app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(users_router, prefix="/users", tags=["Users"])

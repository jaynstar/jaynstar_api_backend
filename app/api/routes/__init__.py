from fastapi import APIRouter
from . import health, auth, ai, weather, resume, user

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(ai.router, prefix="/ai", tags=["ai"])
api_router.include_router(weather.router, prefix="/weather", tags=["weather"])
api_router.include_router(resume.router, prefix="/resume", tags=["resume"])
api_router.include_router(user.router, prefix="/user", tags=["user"])

from fastapi import APIRouter

from src.presentation.api.v1.auth_router import router as auth_router
from src.presentation.api.v1.user_router import router as user_router

api_v1_router = APIRouter(prefix="/api/v1")

api_v1_router.include_router(auth_router)
api_v1_router.include_router(user_router)
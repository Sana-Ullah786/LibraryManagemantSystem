from fastapi import APIRouter

from src.endpoints import auth, user
from src.endpoints.borrowed.router import router as borrowed_router

router = APIRouter()
router.include_router(auth.router)
router.include_router(user.router)
router.include_router(borrowed_router)

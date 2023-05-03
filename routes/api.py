from fastapi import APIRouter

from src.endpoints import auth, author, user

router = APIRouter()
router.include_router(auth.router)
router.include_router(user.router)
router.include_router(author.router)

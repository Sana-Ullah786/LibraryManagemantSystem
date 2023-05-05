from fastapi import APIRouter

from src.endpoints import auth, author, user
from src.endpoints.borrowed.router import router as borrowed_router
from src.endpoints.language import router_init as language_router

router = APIRouter()
router.include_router(auth.router)
router.include_router(language_router.router)
router.include_router(user.router)
router.include_router(author.router)
router.include_router(borrowed_router)

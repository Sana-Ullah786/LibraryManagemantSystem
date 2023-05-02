from fastapi import APIRouter

from src.endpoints import auth, book, copy

router = APIRouter()
router.include_router(auth.router)
router.include_router(copy.router)
router.include_router(book.router)

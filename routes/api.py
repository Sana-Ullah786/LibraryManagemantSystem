from fastapi import APIRouter

from src.endpoints import auth, book, copy, user

router = APIRouter()
router.include_router(auth.router)
router.include_router(copy.router)
router.include_router(book.router)
router.include_router(user.router)

from fastapi import APIRouter

from src.endpoints import auth, author, borrowed, user
from src.endpoints.book import router_init as book_router
from src.endpoints.copy import router_init as copy_router
from src.endpoints.language import router_init as language_router

router = APIRouter()
router.include_router(auth.router)
router.include_router(copy_router.router)
router.include_router(book_router.router)
router.include_router(language_router.router)
router.include_router(user.router)
router.include_router(author.router)
router.include_router(borrowed.router)

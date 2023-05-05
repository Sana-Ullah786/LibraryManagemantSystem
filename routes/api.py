from fastapi import APIRouter

from src.endpoints import auth, user, language, borrowed

router = APIRouter()
router.include_router(auth.router)
router.include_router(language.router)
router.include_router(user.router)
router.include_router(borrowed.router)

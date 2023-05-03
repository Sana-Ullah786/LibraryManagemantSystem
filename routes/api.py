from fastapi import APIRouter

from src.endpoints import auth, user
from src.endpoints.language_api import router_init as language

router = APIRouter()
router.include_router(auth.router)
router.include_router(language.router)
router.include_router(user.router)

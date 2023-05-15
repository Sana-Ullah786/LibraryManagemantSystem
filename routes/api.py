from fastapi import APIRouter

from src.endpoints import auth  # noqa
from src.endpoints import author  # noqa
from src.endpoints import book  # noqa
from src.endpoints import borrowed  # noqa
from src.endpoints import copy  # noqa
from src.endpoints import language  # noqa
from src.endpoints import user  # noqa

router = APIRouter()
router.include_router(auth.router)
router.include_router(language.router)
router.include_router(copy.router)
router.include_router(book.router)
router.include_router(user.router)
router.include_router(author.router)
router.include_router(borrowed.router)

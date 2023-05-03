from fastapi import APIRouter

<<<<<<< HEAD
from src.endpoints import auth, user
from src.endpoints.language_api import router_init as language
=======

from src.endpoints import auth, language
>>>>>>> 17f9945cb7e22f9ece288038c0fc87a8a6468936

router = APIRouter()
router.include_router(auth.router)
router.include_router(language.router)
<<<<<<< HEAD
router.include_router(user.router)
=======
>>>>>>> 17f9945cb7e22f9ece288038c0fc87a8a6468936

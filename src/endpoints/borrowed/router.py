from fastapi import APIRouter

router = APIRouter(
    prefix="/borrowed", tags=["borrowed"], responses={404: {"description": "Not found"}}
)

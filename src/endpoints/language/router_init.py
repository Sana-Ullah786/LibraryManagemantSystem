from fastapi import APIRouter

router = APIRouter(
    prefix="/language",
    tags=["language"],
    responses={404: {"description": "Not found"}},
)

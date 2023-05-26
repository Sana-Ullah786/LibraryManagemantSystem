from fastapi import APIRouter

router = APIRouter(
    prefix="/genre",
    tags=["genre"],
    responses={404: {"description": "Not found"}},
)

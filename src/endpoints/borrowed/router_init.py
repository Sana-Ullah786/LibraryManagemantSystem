from fastapi import APIRouter

router = APIRouter(
    prefix="/borrowed",
    tags=["Borrowed"],
    responses={404: {"description": "Not found"}}
)

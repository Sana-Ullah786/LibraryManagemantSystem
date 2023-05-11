from fastapi import APIRouter

router = APIRouter(
    prefix="/copy", tags=["copy"], responses={401: {"user": "Not authorized"}}
)

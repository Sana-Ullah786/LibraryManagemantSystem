from fastapi import APIRouter

router = APIRouter(
    prefix="/user", tags=["user v2"], responses={401: {"user": "Not authorized"}}
)

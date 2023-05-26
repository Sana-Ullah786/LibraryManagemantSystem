from fastapi import APIRouter

router = APIRouter(
    prefix="/user", tags=["user"], responses={401: {"user": "Not authorized"}}
)

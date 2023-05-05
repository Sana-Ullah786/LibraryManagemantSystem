from fastapi import APIRouter

router = APIRouter(
    prefix="/author", tags=["author"], responses={401: {"user": "Not authorized"}}
)

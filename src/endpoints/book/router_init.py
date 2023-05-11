from fastapi import APIRouter

router = APIRouter(
    prefix="/book", tags=["book"], responses={401: {"book": "Book not Found"}}
)

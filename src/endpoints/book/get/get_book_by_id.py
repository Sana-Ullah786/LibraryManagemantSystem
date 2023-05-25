import logging

from fastapi import Depends
from sqlalchemy import and_, not_, select
from sqlalchemy.orm import Session
from starlette import status

from src.dependencies import get_db
from src.endpoints.book.router_init import router
from src.exceptions import custom_exception
from src.models.book import Book
from src.responses import custom_response


@router.get("/{book_id}", status_code=status.HTTP_200_OK, response_model=None)
async def get_book_by_id(book_id: int, db: Session = Depends(get_db)) -> dict:
    """
    Endpoint to get book by id
    """
    book = (
        db.execute(select(Book).where(and_(Book.id == book_id, not_(Book.is_deleted))))
        .scalars()
        .first()
    )
    if book:
        logging.info(f"Book with id : {book_id} requested")
        return custom_response(
            status_code=status.HTTP_200_OK,
            details="Book fetched successfully!",
            data=book,
        )

    if not book:
        logging.info(f"Book id : {book_id} not Found")
        raise custom_exception(
            status_code=status.HTTP_404_NOT_FOUND, details="Book not found"
        )

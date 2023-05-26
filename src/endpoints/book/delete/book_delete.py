import logging

from fastapi import Depends
from sqlalchemy import and_, not_, select
from sqlalchemy.orm import Session
from starlette import status

from src.dependencies import get_current_librarian, get_db
from src.endpoints.book.router_init import router
from src.exceptions import custom_exception
from src.models.book import Book


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def book_delete(
    book_id: int,
    librarian: dict = Depends(get_current_librarian),
    db: Session = Depends(get_db),
) -> None:
    """
    Delete a book by ID.
    """
    logging.info(
        f"Book with ID: {book_id} Delete Request by Librarian {librarian['id']}"
    )

    book_model = (
        db.execute(select(Book).where(and_(Book.id == book_id, not_(Book.is_deleted))))
        .scalars()
        .first()
    )

    if book_model is None:
        raise custom_exception(
            status_code=status.HTTP_404_NOT_FOUND, details="Book not found"
        )

    logging.info(
        f"Book with ID: {book_model.id} Deleted by Librarian {librarian['id']}"
    )
    book_model.is_deleted = True
    db.commit()

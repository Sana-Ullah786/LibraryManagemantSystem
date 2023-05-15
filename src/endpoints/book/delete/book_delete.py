import logging

from fastapi import Depends, HTTPException
from sqlalchemy import delete, select
from sqlalchemy.orm import Session
from starlette import status

from src.dependencies import get_current_librarian, get_db
from src.endpoints.book.router_init import router
from src.models.book import Book


@router.delete("/{book_id}", status_code=status.HTTP_200_OK)
async def book_delete(
    book_id: int,
    librarian: dict = Depends(get_current_librarian),
    db: Session = Depends(get_db),
) -> dict:
    """
    Delete a book by ID.\n
    Parameters :
    -----------\n
    book_id : Book id (INT), \n
    db : Session \n
    Returns :
    --------- \n
    Book Object

    """
    logging.info(
        f"Book with ID: {book_id} Delete Request by Librarian {librarian['id']}"
    )

    book_model = db.execute(select(Book).where(Book.id == book_id)).scalars().first()

    if book_model is None:
        raise http_exception()

    logging.info(
        f"Book with ID: {book_model.id} Deleted by Librarian {librarian['id']}"
    )

    db.execute(delete(Book).where(Book.id == book_id))
    db.commit()

    return succesful_response()


def http_exception() -> dict:
    return HTTPException(status_code=404, detail="Book not found")


def succesful_response() -> dict:
    return {"status": 201, "transaction": "succesful_response"}

import logging
from datetime import datetime

from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette import status

from src.dependencies import get_current_librarian, get_db
from src.endpoints.book.router_init import router
from src.models.author import Author
from src.models.book import Book
from src.models.genre import Genre
from src.models.language import Language
from src.schemas.book import BookSchema


@router.post("/", status_code=status.HTTP_201_CREATED)
async def book_create(
    book: BookSchema,
    db: Session = Depends(get_db),
    librarian: dict = Depends(get_current_librarian),  # noqa,
) -> dict:
    """
    Endpoint to create a book
    """
    logging.info(f"Book Create Request by Librarian {librarian['id']}")

    language = (
        db.execute(select(Language).where(Language.id == book.language_id))
        .scalars()
        .first()
    )
    authors = (
        db.execute(select(Author).where(Author.id.in_(book.author_ids))).scalars().all()
    )
    genres = (
        db.execute(select(Genre).where(Genre.id.in_(book.genre_ids))).scalars().all()
    )

    book_model = Book()
    book_model.title = book.title
    book_model.date_of_publication = datetime.strptime(
        book.date_of_publication, "%Y-%m-%d"
    ).date()
    book_model.description = book.description
    book_model.isbn = book.isbn
    book_model.language_id = book.language_id
    book_model.authors.extend(authors)
    book_model.genres.extend(genres)
    book_model.language = language

    db.add(book_model)
    db.commit()
    logging.info(
        f"Book with ID: {book_model.id} Created by Librarian {librarian['id']}"
    )

    return succesful_response()


def http_exception() -> dict:
    return HTTPException(status_code=404, detail="Book not found")


def succesful_response() -> dict:
    return {"status": 201, "transaction": "succesful_response"}

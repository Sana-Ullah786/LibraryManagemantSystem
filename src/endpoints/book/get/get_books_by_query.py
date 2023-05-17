import logging
from typing import List

from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette import status

from src.dependencies import get_db
from src.endpoints.book.router_init import router
from src.models.author import Author
from src.models.book import Book
from src.models.genre import Genre
from src.responses import custom_response


@router.get("/", status_code=status.HTTP_200_OK, response_model=None)
async def get_books_by_query(
    author: int = None,
    genre: int = None,
    language: int = None,
    db: Session = Depends(get_db),
) -> dict:
    """
    Endpoint to get books by author , genre , languages
    """
    query = db.query(Book)
    logging.info(f"Book filtered with {author}, {genre},{language}")

    if author is not None:
        authordb = (
            db.execute(select(Author).where(Author.id == author)).scalars().first()
        )
        if authordb is None:
            return http_exception()
        query = query.filter(Book.authors.contains(authordb))

    if genre is not None:
        genredb = db.execute(select(Genre).where(Genre.id == genre)).scalars().first()
        if genredb is None:
            return http_exception()
        query = query.filter(Book.genres.contains(genredb))

    if language is not None:
        query = query.filter(Book.language_id == language)

    books = query.all()
    return custom_response(
        status_code=status.HTTP_200_OK,
        details="Books fetched successfully!",
        data=books,
    )


def http_exception() -> dict:
    return HTTPException(status_code=404, detail="Book not found")


def succesful_response() -> dict:
    return {"status": 201, "transaction": "succesful_response"}

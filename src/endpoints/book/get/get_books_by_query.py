import logging
from typing import Annotated, List

from fastapi import Depends, HTTPException, Query
from sqlalchemy import and_, asc, select
from sqlalchemy.orm import Session
from starlette import status

from src.dependencies import get_db
from src.endpoints.book.router_init import router
from src.exceptions import custom_exception
from src.models.author import Author
from src.models.book import Book
from src.models.genre import Genre
from src.models.language import Language
from src.responses import custom_response


@router.get("/", status_code=status.HTTP_200_OK, response_model=None)
async def get_books_by_query(
    author: int = None,
    genre: int = None,
    language: int = None,
    page_number: Annotated[int, Query(gt=0)] = 1,  # Default value is 1
    page_size: Annotated[int, Query(gt=0)] = 10,  # Default value is 10
    db: Session = Depends(get_db),
) -> dict:
    """
    Endpoint to get books by author , genre , languages
    """
    starting_index = (page_number - 1) * page_size
    query = db.query(Book).order_by(asc(Book.id))
    logging.info(f"Book filtered with {author}, {genre},{language}")

    if author is not None:
        authordb = (
            db.execute(select(Author).where(Author.id == author)).scalars().first()
        )
        if authordb is None:
            return custom_exception(
                status_code=status.HTTP_404_NOT_FOUND, details="Author not found"
            )
        query = query.filter(Book.authors.contains(authordb))

    if genre is not None:
        genredb = db.execute(select(Genre).where(Genre.id == genre)).scalars().first()
        if genredb is None:
            return custom_exception(
                status_code=status.HTTP_404_NOT_FOUND, details="Genre not found"
            )
        query = query.filter(Book.genres.contains(genredb))

    if language is not None:
        languagedb = (
            db.execute(select(Language).where(Language.id == language))
            .scalars()
            .first()
        )
        if languagedb is None:
            return custom_exception(
                status_code=status.HTTP_404_NOT_FOUND, details="Language not found"
            )
        query = query.filter(Book.language_id == language)
    books = query.offset(starting_index).limit(page_size).all()
    return custom_response(
        status_code=status.HTTP_200_OK,
        details="Books fetched successfully!",
        data=books,
    )

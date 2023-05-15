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


@router.get("/", status_code=status.HTTP_200_OK, response_model=None)
async def get_books_by_query(
    author: int = None,
    genre: int = None,
    language: int = None,
    db: Session = Depends(get_db),
) -> List[Book]:
    """
    Endpoint to get books by author , genre , languages \n
    Parameters :
    ----------\n
    author : Author Id ,\n
    genre : Genre Id,\n
    language : Language Id\n
    db : Db Session \n
    Returns :
    ------- \n
    Return List Of Books based on filters . Returns all books if no parameters provided.
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

    return query.all()


def http_exception() -> dict:
    return HTTPException(status_code=404, detail="Book not found")


def succesful_response() -> dict:
    return {"status": 201, "transaction": "succesful_response"}

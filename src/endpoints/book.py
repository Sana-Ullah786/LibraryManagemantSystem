import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from ..models.author import Author
from ..models.book import Book
from ..models.database import get_db
from ..models.genre import Genre
from ..schemas.book import BookSchema

router = APIRouter(
    prefix="/book", tags=["book"], responses={401: {"book": "Book not Found"}}
)


@router.get("/filter/", status_code=status.HTTP_200_OK)
async def get_books_by_query(
    author: int = None,
    genre: int = None,
    language: int = None,
    db: Session = Depends(get_db),
):
    """
    Endpoint to get books by author , genre , languages
    """
    query = db.query(Book)

    if author is not None:
        authordb = db.query(Author).filter(Author.id == author).first()
        if authordb is None:
            return http_exception()
        query = query.filter(Book.authors.contains(authordb))

    if genre is not None:
        genredb = db.query(Genre).filter(Genre.id == genre).first()
        if genredb is None:
            return http_exception()
        query = query.filter(Book.genres.contains(genredb))

    if language is not None:
        query = query.filter(Book.language_id == language)

    return query.all()


@router.get("/{book_id}", status_code=status.HTTP_200_OK)
async def get_book_by_id(book_id: int, db: Session = Depends(get_db)):
    """
    Endpoint to get book by id
    """
    book = db.query(Book).filter(Book.id == book_id).first()
    if book:
        return book
    if not book:
        raise http_exception()
    return book


@router.get("", status_code=status.HTTP_200_OK, response_model=None)
async def filter_book(
    author: str | None = None,
    genre: str | None = None,
    language_id: int | None = None,
    db: Session = Depends(get_db),
) -> None:
    """
    Filters the users list based on param provided. If None given then it will
    return the complete list.
    """
    params = {
        "author": author,
        "genre": genre,
        "language_id": language_id,
    }
    filters = {key: value for key, value in params.items() if value}
    try:
        copies = db.query(Book).filter_by(**filters).all()
        return copies
    except Exception:
        logging.exception(f"Exception occured -- {__name__}.filter_user")
        raise http_exception()


@router.get("/", status_code=status.HTTP_200_OK)
async def get_books(db: Session = Depends(get_db)):
    """
    Endpoint to get all books
    """
    return db.query(Book).all()


@router.post("/", status_code=status.HTTP_201_CREATED)
async def book_create(book: BookSchema, db: Session = Depends(get_db)) -> dict:
    """
    Endpoint to create a book
    """

    book_model = Book()
    book_model.title = book.title
    book_model.date_of_publication = book.date_of_publication
    book_model.description = book.description
    book_model.isbn = book.isbn
    book_model.authors = book.author_ids
    book_model.language_id = book.language_id
    book_model.genres = book.genre_ids

    db.add(book_model)
    db.commit()
    return succesful_response()


@router.put("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def book_update(book_id: int, book: BookSchema, db: Session = Depends(get_db)):
    """
    Update an existing book by ID.
    """

    book_model = db.query(Book).filter(Book.id == book_id).first()

    if book_model is None:
        raise http_exception()

    book_model.title = book.title
    book_model.date_of_publication = book.date_of_publication
    book_model.description = book.description
    book_model.isbn = book.isbn
    book_model.authors = book.author_ids
    book_model.language_id = book.language_id
    book_model.genres = book.genre_ids

    db.add(book_model)
    db.commit()

    return succesful_response()


@router.delete("/delete/{book_id}", status_code=status.HTTP_200_OK)
async def book_delete(book_id: int, db: Session = Depends(get_db)) -> dict:
    """
    Delete a book by ID.
    """

    book_model = db.query(Book).filter(Book.id == book_id).first()

    if book_model is None:
        raise http_exception()

    db.query(Book).filter(Book.id == book_id).delete()

    db.commit()

    return succesful_response()


def http_exception():
    return HTTPException(status_code=404, detail="Book not found")


def succesful_response():
    return {"status": 201, "transaction": "succesful_response"}

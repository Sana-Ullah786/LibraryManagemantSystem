from datetime import datetime
from sqlalchemy import select
from src.endpoints.borrowed.router_init import router
from src.models import all_models
from src.schemas.borrowed import BorrowedSchema
from sqlalchemy.orm import Session
import logging
from src.dependencies import get_current_librarian, get_db

from fastapi import Depends, HTTPException, status


@router.post("/", response_model=BorrowedSchema, status_code=status.HTTP_201_CREATED)
async def create_borrowed(borrowed: BorrowedSchema, user: dict = Depends(get_current_librarian), db: Session = Depends(get_db)) -> BorrowedSchema:
    """
    This function will be used to create a new borrowed.
    Parameters:
        borrowed: The borrowed data.
        db: The database session.
    Returns:
        borrowed: The created borrowed.
    """
    logging.info(f"Creating new borrowed in database with user ID: {borrowed.user_id}")
    try:
        language = all_models.Language(language="English")
        genre = all_models.Genre(genre="Fantasy")
        author = all_models.Author(first_name="J.K.", last_name="Rowling", birth_date=datetime(1980, 1, 1), death_date=None)
        book = all_models.Book(title="Harry Potter", description="The boy who lived", language=language, date_of_publication=datetime(2000, 1, 1), isbn="ABCD-1234")
        book.authors.append(author)
        book.genres.append(genre)
        copy = all_models.Copy(book=book, language=language, status="available")
        user = db.scalar(select(all_models.User).where(all_models.User.email == "email"))
        borrowed = all_models.Borrowed(copy=copy, user=user, issue_date=borrowed.issue_date, due_date=borrowed.due_date, return_date=None)
        db.add_all([language, genre, author, book, copy, borrowed])
        # new_borrowed = all_models.Borrowed()
        # new_borrowed.copy_id = borrowed.copy_id
        # new_borrowed.user_id = borrowed.user_id
        # new_borrowed.issue_date = borrowed.issue_date
        # new_borrowed.due_date = borrowed.due_date
        # new_borrowed.return_date = borrowed.return_date
        # db.add(new_borrowed)
        # db.commit()
        logging.info("Created new borrowed in database with name: " + borrowed.borrowed)
        return borrowed
    except Exception as e:
        logging.exception(
            "Error getting all borroweds from database. Details = " + str(e)
        )
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

import logging

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.dependencies import get_current_librarian, get_db
from src.endpoints.borrowed.router_init import router
from src.models import all_models
from src.schemas.borrowed import BorrowedSchema


@router.post("/", response_model=None, status_code=status.HTTP_201_CREATED)
async def create_borrowed(
    borrowed: BorrowedSchema,
    user: dict = Depends(get_current_librarian),
    db: Session = Depends(get_db),
) -> BorrowedSchema:
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
        new_borrowed = all_models.Borrowed()
        new_borrowed.copy_id = borrowed.copy_id
        new_borrowed.user_id = borrowed.user_id
        new_borrowed.issue_date = borrowed.issue_date
        new_borrowed.due_date = borrowed.due_date
        new_borrowed.return_date = borrowed.return_date
        db.add(new_borrowed)
        db.commit()
        logging.info(
            f"Created new borrowed in database with user ID: {borrowed.user_id}"
        )
        return borrowed
    except Exception as e:
        logging.exception(
            "Error getting all borroweds from database. Details = " + str(e)
        )
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

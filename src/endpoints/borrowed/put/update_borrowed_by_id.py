import logging

from fastapi import Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.dependencies import get_current_librarian, get_db
from src.endpoints.borrowed.router import router
from src.models import all_models
from src.schemas.borrowed import BorrowedSchema


@router.put("/{borrowed_id}", response_model=None, status_code=status.HTTP_200_OK)
async def update_borrowed_by_id(
    borrowed_id: int,
    borrowed: BorrowedSchema,
    db: Session = get_db(),
    librarian=Depends(get_current_librarian),
) -> BorrowedSchema:
    """
    This function will be used to update a borrowed by id.
    Parameters:
        borrowed_id: The id of the borrowed.
        borrowed: The borrowed data.
        librarian: The librarian data. (current librarian)
        db: The database session.
    Returns:
        borrowed: The updated borrowed.
    """
    logging.info("Updating borrowed in database with id: " + str(borrowed_id))
    found_borrowed = db.scalar(
        select(all_models.Borrowed).where(all_models.Borrowed.id == borrowed_id)
    )
    if not found_borrowed:
        logging.warning("Borrowed not found in database with id: " + str(borrowed_id))
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Borrowed not found"
        )
    try:
        found_borrowed.book_id = borrowed.book_id
        found_borrowed.user_id = borrowed.user_id
        found_borrowed.issue_date = borrowed.issue_date
        found_borrowed.due_date = borrowed.due_date
        found_borrowed.return_date = borrowed.return_date
        db.commit()
        logging.info("Updated borrowed in database with id: " + str(borrowed_id))
        borrowed.borrowed_id = borrowed_id
        return borrowed
    except Exception as e:
        logging.exception("Error updating borrowed in database. Details = " + str(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

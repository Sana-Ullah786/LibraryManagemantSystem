import logging

from fastapi import Depends, HTTPException, Path, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.dependencies import get_current_user, get_db
from src.endpoints.borrowed.router_init import router
from src.models import all_models
from src.schemas.borrowed import BorrowedSchema
from src.responses import custom_response


@router.put("/return_borrowed_user/{borrowed_id}", response_model=None, status_code=status.HTTP_200_OK)
async def return_borrowed_for_user( borrowed: BorrowedSchema,
    borrowed_id: int = Path(gt=-1),
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)) -> dict:
    """
    This function will be used to update a borrowed by id.
    Parameters:
        borrowed_id: The id of the borrowed.
        borrowed: The borrowed data.
        user: The user data. (current user)
        db: The database session.
    Returns:
        A dict that contains the status_code, detail and the data.
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
    found_copy = db.scalar(
        select(all_models.Copy).where(all_models.Copy.id == found_borrowed.copy_id)
    )
    if not found_copy:
        logging.warning("Copy not found in database with id: " + str(found_borrowed.copy_id))
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Copy not found"
        )
    try:
        found_borrowed.return_date = borrowed.return_date
        found_copy.status = "available"
        db.commit()
        logging.info("Updated borrowed in database with id: " + str(borrowed_id))
        borrowed.id = borrowed_id
        borrowed.user_id = found_borrowed.user_id
        return custom_response(status_code=status.HTTP_200_OK, details="Borrowed returned successfully", data=borrowed)
    except Exception as e:
        logging.exception("Error updating borrowed in database. Details = " + str(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

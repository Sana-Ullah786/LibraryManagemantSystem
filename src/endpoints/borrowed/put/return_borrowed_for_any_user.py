import logging

from fastapi import Depends, HTTPException, Path, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.dependencies import get_current_librarian, get_db
from src.endpoints.borrowed.router_init import router
from src.exceptions import custom_exception
from src.models import all_models
from src.responses import custom_response
from src.schemas.borrowed import BorrowedSchema
from src.status_constants import AVAILABLE, BORROWED


@router.put(
    "/return_borrowed_any_user/{borrowed_id}",
    response_model=None,
    status_code=status.HTTP_200_OK,
)
async def return_borrowed_for_user(
    borrowed: BorrowedSchema,
    borrowed_id: int = Path(gt=-1),
    db: Session = Depends(get_db),
    librarian: dict = Depends(get_current_librarian),
) -> dict:
    """
    This function will be used to update a borrowed by id.
    Parameters:
        borrowed_id: The id of the borrowed.
        borrowed: The borrowed data.
        librarian: The user data. (current librarian)
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
        raise custom_exception(
            status_code=status.HTTP_404_NOT_FOUND, details="Borrowed not found."
        )
    found_copy = db.scalar(
        select(all_models.Copy).where(all_models.Copy.id == found_borrowed.copy_id)
    )
    if not found_copy:
        logging.warning(
            "Copy not found in database with id: " + str(found_borrowed.copy_id)
        )
        raise custom_exception(
            status_code=status.HTTP_404_NOT_FOUND, details="Copy not found."
        )
    found_status = db.scalar(
        select(all_models.Status).where(all_models.Status.id == found_copy.status_id)
    )
    if not found_status:
        logging.warning(
            "Status not found in database with id: " + str(found_copy.status_id)
        )
        raise custom_exception(
            status_code=status.HTTP_404_NOT_FOUND, details="Status not found."
        )
    if found_status.status != BORROWED:
        logging.warning(
            "Copy is not borrowed in database with id: " + str(found_copy.status_id)
        )
        raise custom_exception(
            status_code=status.HTTP_400_BAD_REQUEST, details="Copy is not borrowed."
        )
    try:
        found_borrowed.return_date = borrowed.return_date
        found_copy.status_id = db.scalars(
            select(all_models.Status.id).where(all_models.Status.status == AVAILABLE)
        ).first()
        db.commit()
        logging.info("Updated borrowed in database with id: " + str(borrowed_id))
        borrowed.id = borrowed_id
        borrowed.user_id = found_borrowed.user_id
        return custom_response(
            status_code=status.HTTP_200_OK,
            details="Borrowed returned successfully",
            data=borrowed,
        )
    except Exception as e:
        logging.exception("Error updating borrowed in database. Details = " + str(e))
        raise custom_exception(
            status_code=status.HTTP_400_BAD_REQUEST,
            details="Error updating borrowed in database. details = " + str(e),
        )

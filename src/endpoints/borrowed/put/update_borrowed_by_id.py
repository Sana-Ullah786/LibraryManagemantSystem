import logging

from fastapi import Depends, Path, status
from sqlalchemy import and_, not_, select
from sqlalchemy.orm import Session

from src.dependencies import get_current_librarian, get_db
from src.endpoints.borrowed.router_init import router
from src.exceptions import custom_exception
from src.models import all_models
from src.responses import custom_response
from src.schemas.borrowed import BorrowedSchema


@router.put("/{borrowed_id}", response_model=None, status_code=status.HTTP_200_OK)
async def update_borrowed_by_id(
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
        librarian: The librarian data. (current librarian)
        db: The database session.
    Returns:
        dict: A dict with the following keys status_code, details and data.
    """
    logging.info("Updating borrowed in database with id: " + str(borrowed_id))
    found_borrowed = db.scalar(
        select(all_models.Borrowed).where(
            and_(
                all_models.Borrowed.id == borrowed_id,
                not_(all_models.Borrowed.is_deleted),
            )
        )
    )
    if not found_borrowed:
        logging.warning("Borrowed not found in database with id: " + str(borrowed_id))
        raise custom_exception(
            status_code=status.HTTP_404_NOT_FOUND, details="Borrowed not found."
        )
    try:
        found_borrowed.due_date = borrowed.due_date
        if borrowed.return_date:
            found_borrowed.return_date = borrowed.return_date
        db.commit()
        logging.info("Updated borrowed in database with id: " + str(borrowed_id))
        borrowed.id = borrowed_id
        borrowed.user_id = found_borrowed.user_id
        return custom_response(
            status_code=status.HTTP_200_OK,
            details="Borrowed updated successfully!",
            data=borrowed,
        )
    except Exception as e:
        logging.exception("Error updating borrowed in database. Details = " + str(e))
        raise custom_exception(
            status_code=status.HTTP_400_BAD_REQUEST,
            details="Error updating borrowed in database. details = " + str(e),
        )

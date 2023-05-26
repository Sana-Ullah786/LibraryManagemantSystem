import logging

from fastapi import Depends, Path, status
from sqlalchemy import and_, not_, select
from sqlalchemy.orm import Session

from src.dependencies import get_current_librarian, get_db
from src.endpoints.borrowed.router_init import router
from src.exceptions import custom_exception
from src.models import all_models
from src.status_constants import AVAILABLE, BORROWED


@router.delete(
    "/{borrowed_id}", response_model=None, status_code=status.HTTP_204_NO_CONTENT
)
async def delete_borrowed(
    borrowed_id: int = Path(gt=-1),
    db: Session = Depends(get_db),
    librarian: dict = Depends(get_current_librarian),
) -> dict:
    """
    This function will be used to delete a borrowed by id.
    Parameters:
        borrowed_id: The id of the borrowed.
        librarian: The librarian data. (current librarian)
        db: The database session.
    Returns:
        dict: A dict with the following keys status_code, details and data.
    """

    logging.info("Deleting borrowed in database with id: " + str(borrowed_id))
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
    found_copy = db.scalar(
        select(all_models.Copy).where(
            and_(
                all_models.Copy.id == found_borrowed.copy_id,
                not_(all_models.Copy.is_deleted),
            )
        )
    )
    if not found_copy:
        logging.warning(
            "Copy not found in database with id: " + str(found_borrowed.copy_id)
        )
        raise custom_exception(
            status_code=status.HTTP_404_NOT_FOUND, details="Copy not found."
        )
    found_status = db.scalar(
        select(all_models.Status).where(
            and_(
                all_models.Status.id == found_copy.status_id,
                not_(all_models.Status.is_deleted),
            )
        )
    )
    if not found_status:
        logging.warning(
            "Status not found in database with id: " + str(found_copy.status_id)
        )
        raise custom_exception(
            status_code=status.HTTP_404_NOT_FOUND, details="Status not found."
        )
    try:
        if found_status.status == BORROWED:
            found_copy.status_id = db.scalar(
                select(all_models.Status.id).where(
                    and_(
                        all_models.Status.status == AVAILABLE,
                        not_(all_models.Status.is_deleted),
                    )
                )
            )
        found_borrowed.is_deleted = True
        db.commit()
        logging.info("Borrowed deleted successfully")
    except Exception as e:
        logging.error("An error occurred: " + str(e))
        raise custom_exception(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            details="An error occurred.",
        )

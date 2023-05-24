import logging

from fastapi import Depends, Path, status
from sqlalchemy import and_, not_, select
from sqlalchemy.orm import Session

from src.dependencies import get_current_librarian, get_db
from src.endpoints.borrowed.router_init import router
from src.exceptions import custom_exception
from src.models import all_models


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
    found_borrowed.is_deleted = True
    db.commit()
    logging.info("Deleted borrowed in database with id: " + str(borrowed_id))

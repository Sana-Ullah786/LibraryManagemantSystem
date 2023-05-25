import logging

from fastapi import Depends, Path
from sqlalchemy import and_, not_, select
from sqlalchemy.orm import Session
from starlette import status

from src.dependencies import get_current_librarian, get_db
from src.endpoints.status.router_init import router
from src.exceptions import custom_exception
from src.models import all_models


@router.delete(
    "/{status_id}", status_code=status.HTTP_204_NO_CONTENT, response_model=None
)
async def status_delete(
    status_id: int = Path(gt=-1),
    db: Session = Depends(get_db),
    librarian=Depends(get_current_librarian),
) -> None:
    """ "
    Deletes the Status on status ID.
    Params
    ------
    JWT token of librarian.\n
    status_id: int
    Returns
    ------
    Status code 204 NO_CONTENT
    """
    logging.info(f"Deleting status {status_id} -- {__name__}")
    found_status = db.scalar(
        select(all_models.Status).where(
            and_(all_models.Status.id == status_id, not_(all_models.Status.is_deleted))
        )
    )
    if not found_status:
        logging.warning("Status not found")
        raise custom_exception(
            status_code=status.HTTP_404_NOT_FOUND, details="Status not found"
        )
    try:
        found_status.is_deleted = True
        db.commit()
        logging.info("Deleted status")
    except Exception as e:
        logging.exception("Error deleting status. Details = " + str(e))
        raise custom_exception(
            status_code=status.HTTP_400_BAD_REQUEST,
            details="Error deleting status. details = " + str(e),
        )

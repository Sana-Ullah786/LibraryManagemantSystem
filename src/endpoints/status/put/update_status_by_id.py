import logging

from fastapi import Depends, HTTPException, Path
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette import status

from src.dependencies import get_current_librarian, get_db
from src.endpoints.status.router_init import router
from src.exceptions import custom_exception
from src.models import all_models
from src.responses import custom_response
from src.schemas.status import StatusSchema


@router.put("/{status_id}", status_code=status.HTTP_200_OK, response_model=None)
async def update_status_by_id(
    status_req: StatusSchema,
    status_id: int = Path(gt=-1),
    db: Session = Depends(get_db),
    librarian=Depends(get_current_librarian),
) -> dict:
    """
    Updates the Status on status ID.
    Parameters:
        status_id: The id of the status.
        status: The status schema.
        db: The database session.
        librarian: The current librarian.
    Returns:
        dict: A dictionary with the status code and message and data.
    """
    logging.info("Updating status by id" + str(status_id))
    found_status = db.scalar(
        select(all_models.Status).where(all_models.Status.id == status_id)
    )
    if not found_status:
        logging.error("Status not found with id" + str(status_id))
        raise custom_exception(
            status_code=status.HTTP_404_NOT_FOUND, details="Status not found"
        )
    try:
        found_status.status = status_req.status
        db.commit()
        status_req.status_id = status_id
        logging.info("Status found")
        return custom_response(
            status_code=status.HTTP_200_OK, details="Success", data=status_req
        )
    except Exception as e:
        logging.error("Error updating status with id" + str(status_id))
        raise custom_exception(
            status_code=status.HTTP_400_BAD_REQUEST,
            details="Error updating status with id" + str(status_id),
        )

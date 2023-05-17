from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from src.dependencies import get_db
from src.endpoints.status.router_init import router
from src.models.status import Status
from src.responses import custom_response


@router.get("/{status_id}", status_code=status.HTTP_200_OK, response_model=None)
async def get_status_by_id(status_id: int, db: Session = Depends(get_db)) -> dict:
    """
    This function will be used to get a status by id.
    Parameters:
        status_id: The id of the status.
        db: The database session.
    Returns:
        dict: A dictionary with the status code and message and data.
    """
    status = db.execute(Status).filter(Status.id == status_id).first()
    if not status:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Status not found"
        )
    return custom_response(
        status_code=status.HTTP_200_OK, details="Status found", data=status
    )

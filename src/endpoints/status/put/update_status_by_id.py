from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from src.dependencies import get_current_librarian, get_db
from src.endpoints.status.router_init import router
from src.models.status import Status
from src.responses import custom_response
from src.schemas.status import StatusSchema


@router.put("/{status_id}", status_code=status.HTTP_200_OK, response_model=None)
async def update_status_by_id(
    status_id: int,
    status: StatusSchema,
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
    status_model = db.execute(Status).filter(Status.id == status_id).first()
    if not status_model:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Status not found"
        )
    try:
        status_model.status = status.status
        db.commit()
        return custom_response(
            status_code=status.HTTP_200_OK, details="Success", data=status_model
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

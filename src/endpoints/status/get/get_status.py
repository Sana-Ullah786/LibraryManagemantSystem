import logging

from fastapi import Depends
from sqlalchemy import not_, select
from sqlalchemy.orm import Session
from starlette import status

from src.dependencies import get_db
from src.endpoints.status.router_init import router
from src.models import all_models
from src.responses import custom_response


@router.get("/", status_code=status.HTTP_200_OK, response_model=None)
async def get_status(db: Session = Depends(get_db)) -> dict:
    """
    Get all statuses.
    Parameters:
        db: The database session.
    Returns:
        dict: A dict with the following keys status_code, details and data.
    """
    statuses = db.scalars(
        select(all_models.Status).where(not_(all_models.Status.is_deleted))
    ).all()
    logging.info("Fetching all statuses")
    return custom_response(
        status_code=status.HTTP_200_OK, details="Success", data=statuses
    )

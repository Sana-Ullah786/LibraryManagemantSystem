import logging
from typing import List

from fastapi import Depends, status
from sqlalchemy import not_, select
from sqlalchemy.orm import Session

from src.dependencies import get_db
from src.endpoints.genre.router_init import router
from src.exceptions import custom_exception
from src.models import all_models
from src.responses import custom_response


@router.get("/", response_model=None, status_code=status.HTTP_200_OK)
async def get_all_genre(db: Session = Depends(get_db)) -> dict:
    """
    This function will be used to get all the Genre.
    Parameters:
        db: The database session.
    Returns:
        dict: status code and message and data.
    """
    logging.info("Getting all genre")
    try:
        all_genre = db.scalars(
            select(all_models.Genre).where(not_(all_models.Genre.is_deleted))
        ).all()
        return custom_response(
            status_code=status.HTTP_200_OK, details="All genre found", data=all_genre
        )
    except Exception as e:
        logging.exception("Error getting all genre from database. Details = " + str(e))
        raise custom_exception(
            status_code=status.HTTP_400_BAD_REQUEST,
            details="Error getting all genre from database. details = " + str(e),
        )

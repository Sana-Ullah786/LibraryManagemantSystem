import logging
from typing import List

from fastapi import Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.dependencies import get_db
from src.endpoints.genre.router_init import router
from src.models import all_models


@router.get("/", response_model=None, status_code=status.HTTP_200_OK)
async def get_all_genre(db: Session = Depends(get_db)) -> List[all_models.Genre]:
    """
    This function will be used to get all the Genre.
    Parameters:
        db: The database session.
    Returns:
        genre: The list of all genre.
    """
    logging.info("Getting all genre")
    try:
        all_genre = db.scalars(select(all_models.Genre)).all()
        return all_genre
    except Exception as e:
        logging.exception("Error getting all genre from database. Details = " + str(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

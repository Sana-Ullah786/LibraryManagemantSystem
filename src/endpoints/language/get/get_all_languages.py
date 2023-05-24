import logging
from typing import List

from fastapi import Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.dependencies import get_db
from src.endpoints.language.router_init import router
from src.exceptions import custom_exception
from src.models import all_models
from src.responses import custom_response


@router.get("/", response_model=None, status_code=status.HTTP_200_OK)
async def get_all_languages(db: Session = Depends(get_db)) -> dict:
    """
    This function will be used to get all the languages.
    Parameters:
        db: The database session.
    Returns:
        dict: The list of all languages.
    """
    logging.info("Getting all languages")
    try:
        all_languages = db.scalars(select(all_models.Language)).all()
        return custom_response(
            status_code=status.HTTP_200_OK,
            details="All languages found",
            data=all_languages,
        )
    except Exception as e:
        logging.exception(
            "Error getting all languages from database. Details = " + str(e)
        )
        raise custom_exception(
            status_code=status.HTTP_400_BAD_REQUEST,
            details="Error getting all languages from database. details = " + str(e),
        )

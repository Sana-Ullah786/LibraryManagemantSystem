import logging
from typing import List

from fastapi import Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from ....dependencies import get_db
from ....models import all_models
from ..router_init import router


@router.get("/", response_model=None, status_code=status.HTTP_200_OK)
async def get_all_languages(db: Session = Depends(get_db)) -> List[all_models.Language]:
    """
    This function will be used to get all the languages.
    Parameters:
        db: The database session.
    Returns:
        languages: The list of all languages.
    """
    logging.info("Getting all languages")
    try:
        all_languages = db.scalars(select(all_models.Language)).all()
        return all_languages
    except Exception as e:
        logging.exception(
            "Error getting all languages from database. Details = " + str(e)
        )
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

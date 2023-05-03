import logging
from typing import List

from fastapi import Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.endpoints.auth import get_current_librarian
from src.models import all_models
from src.models.database import get_db

from .router_init import router


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


@router.get("/{language_id}", response_model=None, status_code=status.HTTP_200_OK)
async def get_language_by_id(
    language_id: int,
    user: dict = Depends(get_current_librarian),
    db: Session = Depends(get_db),
) -> all_models.Language:
    """
    This function will be used to get a language by id.
    Parameters:
        language_id: The id of the language.
        user: The user data. (current libarian)
        db: The database session.
    Returns:
        language: The language.
    """
    logging.info("Getting language by id = " + str(language_id) + " from database")
    language = db.scalars(
        select(all_models.Language).where(all_models.Language.id == language_id)
    ).first()
    if not language:
        logging.warning("Language not found in database")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Language not found"
        )
    logging.info("Language found in database and returned")
    return language

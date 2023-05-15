import logging

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.dependencies import get_current_librarian, get_db
from src.endpoints.language.router_init import router
from src.models import all_models
from src.schemas import language_schema


@router.post("/", response_model=None, status_code=status.HTTP_201_CREATED)
async def create_language(
    language: language_schema.LanguageSchema,
    user: dict = Depends(get_current_librarian),
    db: Session = Depends(get_db),
) -> language_schema.LanguageSchema:
    """
    This function will be used to create a new language.
    Parameters:
        language: The language data.
        db: The database session.
    Returns:
        language: The created language.
    """
    logging.info("Creating new language in database with name: " + language.language)
    try:
        new_language = all_models.Language()
        new_language.language = language.language
        db.add(new_language)
        db.commit()
        db.refresh(new_language)
        logging.info("Created new language in database with name: " + language.language)
        language.language_id = new_language.id
        return language
    except Exception as e:
        logging.exception(
            "Error getting all languages from database. Details = " + str(e)
        )
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

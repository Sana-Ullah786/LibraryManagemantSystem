import logging

from fastapi import Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from ....dependencies import get_current_librarian, get_db
from ....models import all_models
from ....schemas import language_schema
from ..router_init import router


@router.put("/{language_id}", response_model=None, status_code=status.HTTP_200_OK)
async def update_language_by_id(
    language_id: int,
    language: language_schema.LanguageSchema,
    user: dict = Depends(get_current_librarian),
    db: Session = Depends(get_db),
) -> language_schema.LanguageSchema:
    """
    This function will be used to update a language by id.
    Parameters:
        language_id: The id of the language.
        language: The language data.
        user: The user data. (current librarian)
        db: The database session.
    Returns:
        language: The updated language.
    """
    logging.info("Updating language in database with id: " + str(language_id))
    found_language = db.scalar(
        select(all_models.Language).where(all_models.Language.id == language_id)
    )
    if not found_language:
        logging.warning("Language not found in database")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Language not found"
        )
    try:
        found_language.language = language.language
        db.commit()
        logging.info("Updated language in database with id: " + str(language_id))
        language.language_id = language_id
        return language
    except Exception as e:
        logging.exception("Error updating language in database. Details = " + str(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

import logging

from fastapi import Depends, Path, status
from sqlalchemy import and_, not_, select
from sqlalchemy.orm import Session

from src.dependencies import get_current_librarian, get_db
from src.endpoints.language.router_init import router
from src.exceptions import custom_exception
from src.models import all_models
from src.responses import custom_response
from src.schemas import language_schema


@router.put("/{language_id}", response_model=None, status_code=status.HTTP_200_OK)
async def update_language_by_id(
    language: language_schema.LanguageSchema,
    language_id: int = Path(gt=-1),
    user: dict = Depends(get_current_librarian),
    db: Session = Depends(get_db),
) -> dict:
    """
    This function will be used to update a language by id.
    Parameters:
        language_id: The id of the language.
        language: The language data.
        user: The user data. (current librarian)
        db: The database session.
    Returns:
        dict: A dictionary with the status code and message and data.
    """
    logging.info("Updating language in database with id: " + str(language_id))
    found_language = db.scalar(
        select(all_models.Language).where(
            and_(
                all_models.Language.id == language_id,
                not_(all_models.Language.is_deleted),
            )
        )
    )
    if not found_language:
        logging.warning("Language not found in database")
        raise custom_exception(
            status_code=status.HTTP_404_NOT_FOUND, details="Language not found."
        )
    try:
        found_language.language = language.language
        db.commit()
        logging.info("Updated language in database with id: " + str(language_id))
        language.language_id = language_id
        return custom_response(
            status_code=status.HTTP_200_OK, details="Language updated", data=language
        )
    except Exception as e:
        logging.exception("Error updating language in database. Details = " + str(e))
        raise custom_exception(
            status_code=status.HTTP_400_BAD_REQUEST,
            details="Error updating language in database. details = " + str(e),
        )

import logging

from fastapi import Depends, HTTPException, Path, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.dependencies import get_current_user, get_db
from src.endpoints.language.router_init import router
from src.models import all_models


@router.get("/{language_id}", response_model=None, status_code=status.HTTP_200_OK)
async def get_language_by_id(
    language_id: int = Path(gt=-1),
    user: dict = Depends(get_current_user),
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

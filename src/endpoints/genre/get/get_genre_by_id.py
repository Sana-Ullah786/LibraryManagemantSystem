import logging

from fastapi import Depends, Path, status
from sqlalchemy import and_, not_, select
from sqlalchemy.orm import Session

from src.dependencies import get_db
from src.endpoints.genre.router_init import router
from src.exceptions import custom_exception
from src.models import all_models
from src.responses import custom_response


@router.get("/{genre_id}", response_model=None, status_code=status.HTTP_200_OK)
async def get_genre_by_id(
    genre_id: int = Path(gt=-1),
    db: Session = Depends(get_db),
) -> dict:
    """
    This function will be used to get a Genre by id.
    Parameters:
        genre_id: The id of the genre.
        user: The user data. (current libarian)
        db: The database session.
    Returns:
        dict: A dictionary with the status code and message and data.
    """
    logging.info("Getting genre by id = " + str(genre_id) + " from database")
    genre = db.scalars(
        select(all_models.Genre).where(
            and_(all_models.Genre.id == genre_id, not_(all_models.Genre.is_deleted))
        )
    ).first()
    if not genre:
        logging.warning("genre not found in database")
        raise custom_exception(
            status_code=status.HTTP_404_NOT_FOUND, details="Genre not found."
        )
    logging.info("Genre found in database and returned")
    return custom_response(
        status_code=status.HTTP_200_OK, details="Genre found", data=genre
    )

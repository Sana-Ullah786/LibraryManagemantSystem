import logging

from fastapi import Depends, Path, status
from sqlalchemy import and_, not_, select
from sqlalchemy.orm import Session

from src.dependencies import get_current_librarian, get_db
from src.endpoints.genre.router_init import router
from src.exceptions import custom_exception
from src.models import all_models
from src.responses import custom_response
from src.schemas import genre


@router.put("/{genre_id}", response_model=None, status_code=status.HTTP_200_OK)
async def update_genre_by_id(
    new_genre: genre.GenreSchema,
    genre_id: int = Path(gt=-1),
    user: dict = Depends(get_current_librarian),
    db: Session = Depends(get_db),
) -> dict:
    """
    This function will be used to update a genre by id.
    Parameters:
        new_genre: The new genre data.
        genre_id: The id of the genre.
        user: The user data. (current libarian)
        db: The database session.
    Returns:
        dict: A dictionary with the status code and message and data.
    """
    logging.info("Updating genre in database with id: " + str(genre_id))
    found_genre = db.scalar(
        select(all_models.Genre).where(
            and_(all_models.Genre.id == genre_id, not_(all_models.Genre.is_deleted))
        )
    )
    if not found_genre:
        logging.warning("Genre not found in database")
        raise custom_exception(
            status_code=status.HTTP_404_NOT_FOUND, details="Genre not found."
        )
    try:
        found_genre.genre = new_genre.genre
        db.commit()
        logging.info("Updated Genre in database with id: " + str(genre_id))
        new_genre.id = genre_id
        return custom_response(
            status_code=status.HTTP_200_OK,
            details="Genre updated successfully!",
            data=new_genre,
        )
    except Exception as e:
        logging.exception("Error updating Genre in database. Details = " + str(e))
        raise custom_exception(
            status_code=status.HTTP_400_BAD_REQUEST,
            details="Error updating Genre in database. details = " + str(e),
        )

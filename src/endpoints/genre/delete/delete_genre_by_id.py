import logging

from fastapi import Depends, HTTPException, Path, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.dependencies import get_current_librarian, get_db
from src.endpoints.genre.router_init import router
from src.exceptions import custom_exception
from src.models import all_models


@router.delete(
    "/{genre_id}", response_model=None, status_code=status.HTTP_204_NO_CONTENT
)
async def delete_genre_by_id(
    genre_id: int = Path(gt=-1),
    user: dict = Depends(get_current_librarian),
    db: Session = Depends(get_db),
) -> None:
    """
    This function will be used to delete a genre by id.
    Parameters:
        genre_id: The id of the genre.
        user: The user data. (current librarian)
        db: The database session.
    Returns:
        None
    """
    logging.info("Deleting genre in database with id: " + str(genre_id))
    found_genre = db.scalars(
        select(all_models.Genre).where(all_models.Genre.id == genre_id)
    ).first()
    if not found_genre:
        logging.warning("Genre not found in database")
        raise custom_exception(
            status_code=status.HTTP_404_NOT_FOUND, details="Genre not found."
        )
    try:
        db.delete(found_genre)
        db.commit()
        logging.info("Deleted Genre in database with id: " + str(genre_id))
    except Exception as e:
        logging.exception("Error deleting Genre from database. Details = " + str(e))
        raise custom_exception(
            status_code=status.HTTP_400_BAD_REQUEST,
            details="Error deleting Genre from database. details = " + str(e),
        )

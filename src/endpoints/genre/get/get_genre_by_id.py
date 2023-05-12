import logging

from fastapi import Depends, HTTPException, Path, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.dependencies import get_current_user, get_db
from src.endpoints.genre.router_init import router
from src.models import all_models


@router.get("/{genre_id}", response_model=None, status_code=status.HTTP_200_OK)
async def get_genre_by_id(
    genre_id: int = Path(gt=-1),
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> all_models.Genre:
    """
    This function will be used to get a Genre by id.
    Parameters:
        genre_id: The id of the genre.
        user: The user data. (current libarian)
        db: The database session.
    Returns:
        genre: The genre.
    """
    logging.info("Getting genre by id = " + str(genre_id) + " from database")
    genre = db.scalars(
        select(all_models.Genre).where(all_models.Genre.id == genre_id)
    ).first()
    if not genre:
        logging.warning("genre not found in database")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Genre not found"
        )
    logging.info("Genre found in database and returned")
    return genre

import logging

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.dependencies import get_current_librarian, get_db
from src.endpoints.genre.router_init import router
from src.models import all_models
from src.responses import custom_response
from src.schemas import genre


@router.post("/", response_model=None, status_code=status.HTTP_201_CREATED)
async def create_genre(
    new_genre: genre.GenreSchema,
    user: dict = Depends(get_current_librarian),
    db: Session = Depends(get_db),
) -> dict:
    """
    This function will be used to create a new genre.
    Parameters:
        new_genre: The genre data.
        user: The user data. (current libarian)
        db: The database session.
    Returns:
        dict: A dictionary with the status code and message and data.
    """
    logging.info("Creating new Genre in database with name: " + new_genre.genre)
    try:
        genre_model = all_models.Genre()
        genre_model.genre = new_genre.genre
        db.add(genre_model)
        db.commit()
        db.refresh(genre_model)
        logging.info("Created new Genre in database with name: " + new_genre.genre)
        new_genre.id = genre_model.id
        return custom_response(
            status_code=status.HTTP_201_CREATED,
            details="Genre created successfully!",
            data=new_genre,
        )
    except Exception as e:
        logging.exception("Error creating a new genre database. Details = " + str(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

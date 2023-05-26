import logging

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette import status

from src.dependencies import get_current_librarian, get_db
from src.endpoints.author.router_init import router
from src.models.author import Author
from src.responses import custom_response
from src.schemas.author_schema import AuthorSchema


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=None)
async def create_author(
    author: AuthorSchema,
    user: dict = Depends(get_current_librarian),
    db: Session = Depends(get_db),
) -> dict:
    """
    Adds new author to the database.\n
    Params
    ------
    JWT token of librarian.\n
    Author json object as of pydantic model\n
    Returns
    ------
    dict : A dict with status code, details and data
    """
    author_model = Author(**author.dict())
    db.add(author_model)
    logging.info(f"Inserting new author -- {__name__}")
    db.commit()
    db.refresh(author_model)
    author.id = author_model.id
    return custom_response(
        status_code=status.HTTP_201_CREATED,
        details="Author created successfully!",
        data=author,
    )

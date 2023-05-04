import logging

from fastapi import Depends, HTTPException, Path
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette import status

from ....dependencies import get_current_librarian, get_db
from ....models.author import Author
from ....schemas.author_schema import AuthorSchema
from ..router_init import router


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=None)
def create_author(
    author: AuthorSchema,
    user: dict = Depends(get_current_librarian),
    db: Session = Depends(get_db),
) -> AuthorSchema:
    """
    Adds new author to the database.\n
    Params
    ------
    JWT token of librarian.\n
    Author json object as of pydantic model\n
    Returns
    ------
    Author model after insertion.
    """
    author_model = Author(**author.dict())
    db.add(author_model)
    logging.info(f"Inserting new author -- {__name__}")
    db.commit()
    return author

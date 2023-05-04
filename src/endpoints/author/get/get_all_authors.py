import logging
from typing import List

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette import status

from src.dependencies import get_current_user, get_db
from src.endpoints.author.router_init import router
from src.models.author import Author


@router.get("/", status_code=status.HTTP_200_OK, response_model=None)
def get_all_authors(
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> List[Author]:
    """
    Returns all the Authors in DB.\n
    Params
    ------
    JWT token of user.\n
    Returns
    ------
    List of authors
    """
    logging.info(f"Getting all the authors -- {__name__}")
    authors = db.execute(select(Author)).scalars().all()
    return authors

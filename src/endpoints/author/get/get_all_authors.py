import logging
from typing import Annotated, List

from fastapi import Depends, Query
from sqlalchemy import asc, select
from sqlalchemy.orm import Session
from starlette import status

from src.dependencies import get_current_user, get_db
from src.endpoints.author.router_init import router
from src.models.author import Author


@router.get("/", status_code=status.HTTP_200_OK, response_model=None)
async def get_all_authors(
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
    page_number: Annotated[int, Query(gt=0)] = 1,  # Default value is 1
    page_size: Annotated[int, Query(gt=0)] = 10,  # Default value is 10
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
    starting_index = (page_number - 1) * page_size
    ending_index = starting_index + page_size
    logging.info(f"Getting all the authors -- {__name__}")
    authors = (
        db.execute(
            select(Author)
            .order_by(asc(Author.id))
            .offset(starting_index)
            .limit(ending_index)
        )
        .scalars()
        .all()
    )
    return authors

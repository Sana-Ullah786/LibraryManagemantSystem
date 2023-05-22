import logging

from fastapi import Depends, HTTPException, Path
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette import status

from src.dependencies import get_db
from src.endpoints.author.router_init import router
from src.exceptions import custom_exception
from src.models.author import Author
from src.responses import custom_response


@router.get("/{author_id}", status_code=status.HTTP_200_OK, response_model=None)
async def get_authors_by_id(
    author_id: int = Path(gt=0),
    db: Session = Depends(get_db),
) -> dict:
    """
    Returns the Authors having the id passed as param.\n
    Params
    ------
    JWT token of user.\n
    author_id: int
    Returns
    ------
    dict : A dict with status code, details and data
    """
    logging.info(f"Getting authors {author_id}-- {__name__}")
    author = db.execute(select(Author).where(Author.id == author_id)).scalars().first()
    if not author:
        logging.error("Author not found -- {__name__}")
        raise custom_exception(
            status_code=status.HTTP_404_NOT_FOUND, details="Author not found."
        )
    return custom_response(
        status_code=status.HTTP_200_OK,
        details="Author fetched successfully!",
        data=author,
    )

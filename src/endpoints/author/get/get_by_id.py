import logging

from fastapi import Depends, HTTPException, Path
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette import status

from src.dependencies import get_current_user, get_db
from src.endpoints.author.router_init import router
from src.models.author import Author


@router.get("/{author_id}", status_code=status.HTTP_200_OK, response_model=None)
async def get_authors_by_id(
    author_id: int = Path(gt=0),
    db: Session = Depends(get_db),
) -> Author:
    """
    Returns the Authors having the id passed as param.\n
    Params
    ------
    JWT token of user.\n
    author_id: int
    Returns
    ------
    Author
    """
    logging.info(f"Getting authors {author_id}-- {__name__}")
    author = db.execute(select(Author).where(Author.id == author_id)).scalars().first()
    if not author:
        logging.error("Author not found -- {__name__}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Author not found!"
        )
    return author

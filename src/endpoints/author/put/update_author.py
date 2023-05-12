import logging

from fastapi import Depends, HTTPException, Path
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette import status

from src.dependencies import get_current_librarian, get_db
from src.endpoints.author.router_init import router
from src.models.author import Author
from src.schemas.author_schema import AuthorSchema


@router.put("/{author_id}", status_code=status.HTTP_200_OK, response_model=None)
async def update_author(
    new_author: AuthorSchema,
    author_id: int = Path(gt=0),
    user: dict = Depends(get_current_librarian),
    db: Session = Depends(get_db),
) -> AuthorSchema:
    """
    Updates the author with new detail whose id is passed.\n
    Params
    ------
    JWT token of librarian.\n
    Author json object as of pydantic model\n
    author_id: int = id of author to update
    Returns
    ------
    Updated author model.
    """
    logging.info(f"Getting author {author_id}-- {__name__}")
    author = db.execute(select(Author).where(Author.id == author_id)).scalars().first()
    if not author:
        logging.error("Author not found -- {__name__}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Author not found!"
        )
    author.first_name = new_author.first_name
    author.last_name = new_author.last_name
    author.birth_date = new_author.birth_date
    author.death_date = new_author.death_date
    logging.info(f"updating author {author_id}-- {__name__}")
    db.commit()
    db.refresh(author)
    new_author.id = author.id
    return new_author

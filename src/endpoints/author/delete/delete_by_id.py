import logging

from fastapi import Depends, HTTPException, Path
from sqlalchemy import and_, not_, select
from sqlalchemy.orm import Session
from starlette import status

from src.dependencies import get_current_librarian, get_db
from src.endpoints.author.router_init import router
from src.exceptions import custom_exception
from src.models.author import Author


@router.delete(
    "/{author_id}", status_code=status.HTTP_204_NO_CONTENT, response_model=None
)
async def delete_author_by_id(
    author_id: int = Path(gt=0),
    user: dict = Depends(get_current_librarian),
    db: Session = Depends(get_db),
) -> None:
    """
    Deletes the authors whose id is passed.
    Params
    ------
    JWT token of librarian.\n
    author_id: int
    Returns
    ------
    Status code 204 NO_CONTENT
    """
    author = (
        db.execute(
            select(Author).where(and_(Author.id == author_id, not_(Author.is_deleted)))
        )
        .scalars()
        .first()
    )
    if not author:
        logging.error("Author not found -- {__name__}")
        raise custom_exception(
            status_code=status.HTTP_404_NOT_FOUND, details="Author not found."
        )
    author.is_deleted = True
    logging.info(f"Deleting author {author_id} -- {__name__}")
    db.commit()

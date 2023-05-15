import logging
from typing import List

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette import status

from src.dependencies import get_db
from src.endpoints.copy.router_init import router
from src.models.copy import Copy


@router.get("/book/{book_id}", status_code=status.HTTP_200_OK, response_model=None)
async def get_copies_by_book_id(
    book_id: int, db: Session = Depends(get_db)
) -> List[Copy]:
    """
    Endpoint to get all copies by book id
    \n
    Parameter:
    ----------\n
    book_id : Book id of the book to get copies of . \n
    db : Db session .\n
    Returns:
    -------- \n
    list of books under book id.

    """
    copies = (
        db.execute(select(Copy).where(Copy.book_id == book_id)).unique().scalars().all()
    )
    if copies:
        logging.info(f"Copies with book id : {book_id}")
        return copies
    logging.info(f"No Copy with book id : {book_id}")
    return copies

import logging
from typing import List

from fastapi import Depends
from sqlalchemy import and_, not_, select
from sqlalchemy.orm import Session
from starlette import status

from src.dependencies import get_db
from src.endpoints.copy.router_init import router
from src.exceptions import custom_exception
from src.models.copy import Copy
from src.responses import custom_response


@router.get("/book/{book_id}", status_code=status.HTTP_200_OK, response_model=None)
async def get_copies_by_book_id(book_id: int, db: Session = Depends(get_db)) -> dict:
    """
    Endpoint to get all copies by book id
    """
    copies = (
        db.execute(
            select(Copy).where(and_(Copy.book_id == book_id, not_(Copy.is_deleted)))
        )
        .unique()
        .scalars()
        .all()
    )
    if copies:
        logging.info(f"Copies with book id : {book_id}")
        return custom_response(
            status_code=status.HTTP_200_OK, details="Copies found", data=copies
        )
    logging.info(f"No Copy with book id : {book_id}")
    raise custom_exception(
        status_code=status.HTTP_404_NOT_FOUND, details="No Copies found"
    )

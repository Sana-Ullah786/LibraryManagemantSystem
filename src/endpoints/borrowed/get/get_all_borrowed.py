import logging
from typing import List

from fastapi import Depends, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.dependencies import get_current_librarian, get_db
from src.endpoints.borrowed.router_init import router
from src.models.borrowed import Borrowed
from src.responses import custom_response


@router.get("/", status_code=status.HTTP_200_OK, response_model=None)
async def get_all_borrowed(
    librarian: dict = Depends(get_current_librarian), db: Session = Depends(get_db)
) -> dict:
    """
    Returns all borrowed objects. Only accessible by librarian
    """

    logging.info(f"Librarian {librarian['id']} requested all borrowed.")

    borrowed = db.scalars(select(Borrowed)).unique().all()
    return custom_response(
        status_code=status.HTTP_200_OK,
        details="Borrowed fetched successfully!",
        data=borrowed,
    )

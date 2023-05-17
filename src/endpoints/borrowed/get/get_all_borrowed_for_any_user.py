import logging
from typing import List

from fastapi import Depends, Path, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.dependencies import get_current_librarian, get_db
from src.endpoints.borrowed.router_init import router
from src.models.borrowed import Borrowed
from src.responses import custom_response


@router.get("/user/{user_id}", status_code=status.HTTP_200_OK, response_model=None)
async def get_all_borrowed_for_any_user(
    user_id: int = Path(gt=-1),
    librarian: dict = Depends(get_current_librarian),
    db: Session = Depends(get_db),
) -> dict:
    """
    Returns all borrowed objects for a specific user. Can only be used by librarian.
    """

    logging.info(
        f"Librarian with id {librarian['id']} requested all borrowed books for user with id {user_id}."
    )

    all_borrowed = (
        db.scalars(select(Borrowed).where(Borrowed.user_id == user_id)).unique().all()
    )
    return custom_response(status_code=status.HTTP_200_OK, details="Fetched All Borrowed",data=all_borrowed)

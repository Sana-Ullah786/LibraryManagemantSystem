import logging
from typing import List

from fastapi import Depends, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.dependencies import get_current_librarian, get_current_user, get_db
from src.endpoints.borrowed.router import router
from src.models.borrowed import Borrowed


@router.get("/user", status_code=status.HTTP_200_OK, response_model=None)
async def get_all_borrowed_for_logged_in_user(
    user: dict = Depends(get_current_user), db: Session = Depends(get_db)
) -> List[Borrowed]:
    """
    Returns all borrowed objects for the logged in user.
    """

    logging.info(f"User with id {user['id']} requested all of their borrowed books.")

    return db.scalars(select(Borrowed).where(Borrowed.user_id == user["id"])).all()

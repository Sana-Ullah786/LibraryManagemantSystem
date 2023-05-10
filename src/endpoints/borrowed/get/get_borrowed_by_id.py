import logging
from typing import List

from fastapi import Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.dependencies import get_current_user, get_db
from src.endpoints.borrowed.router_init import router
from src.models.borrowed import Borrowed
from src.models.user import User


@router.get("/{borrowed_id}", status_code=status.HTTP_200_OK, response_model=None)
async def get_borrowed_by_id(
    borrowed_id: int,
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> List[Borrowed]:
    """
    Returns a single borrowed object. Librarian can access any, while a user can only access their own.
    """

    logging.info(f"User with id {user['id']} requested borrowed with id {borrowed_id}.")

    query = select(Borrowed).where(Borrowed.id == borrowed_id)
    if not db.scalar(select(User).where(User.id == user["id"])).is_librarian:
        query = query.where(Borrowed.user_id == user["id"])

    borrowed = db.scalar(query)
    if borrowed is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Borrowed not found"
        )
    return borrowed

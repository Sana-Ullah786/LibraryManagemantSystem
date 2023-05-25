import logging
from typing import Annotated, List

from fastapi import Depends, Path, Query, status
from sqlalchemy import and_, not_, asc, select
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
    page_number: Annotated[int, Query(gt=0)] = 1,  # Default value is 1
    page_size: Annotated[int, Query(gt=0)] = 10,  # Default value is 10
) -> dict:
    """
    Returns all borrowed objects for a specific user. Can only be used by librarian.
    """

    logging.info(
        f"Librarian with id {librarian['id']} requested all borrowed books for user with id {user_id}."
    )
    starting_index = (page_number - 1) * page_size
    all_borrowed = (
        db.scalars(
            select(Borrowed)
            .where(Borrowed.user_id == user_id)
            .order_by(asc(Borrowed.id))
            .offset(starting_index)
            .limit(page_size)
        )
        .unique()
        .all()
    )
    return custom_response(
        status_code=status.HTTP_200_OK,
        details="Fetched All Borrowed",
        data=all_borrowed,
    )

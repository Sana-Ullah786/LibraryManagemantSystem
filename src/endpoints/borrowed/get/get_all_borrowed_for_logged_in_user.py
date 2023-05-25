import logging
from typing import Annotated, List

from fastapi import Depends, Query, status
from sqlalchemy import and_, asc, not_, select
from sqlalchemy.orm import Session

from src.dependencies import get_current_user, get_db
from src.endpoints.borrowed.router_init import router
from src.models.borrowed import Borrowed
from src.responses import custom_response


@router.get("/user", status_code=status.HTTP_200_OK, response_model=None)
async def get_all_borrowed_for_logged_in_user(
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
    page_number: Annotated[int, Query(gt=0)] = 1,  # Default value is 1
    page_size: Annotated[int, Query(gt=0)] = 10,  # Default value is 10
) -> dict:
    """
    Returns all borrowed objects for the logged in user.
    """

    logging.info(f"User with id {user['id']} requested all of their borrowed books.")
    starting_index = (page_number - 1) * page_size
    all_borrowed = (
        db.scalars(
            select(Borrowed)
            .where(and_(Borrowed.user_id == user["id"], not_(Borrowed.is_deleted)))
            .order_by(asc(Borrowed.id))
            .offset(starting_index)
            .limit(page_size)
        )
        .unique()
        .all()
    )
    return custom_response(
        status_code=status.HTTP_200_OK,
        details="Borrowed fetched successfully!",
        data=all_borrowed,
    )

import logging
from typing import Annotated, List

from fastapi import Depends, Query, status
from sqlalchemy import asc, select
from sqlalchemy.orm import Session

from src.dependencies import get_current_librarian, get_db
from src.endpoints.borrowed.router_init import router
from src.models.borrowed import Borrowed
from src.responses import custom_response


@router.get("/", status_code=status.HTTP_200_OK, response_model=None)
async def get_all_borrowed(
    librarian: dict = Depends(get_current_librarian),
    db: Session = Depends(get_db),
    page_number: Annotated[int, Query(gt=0)] = 1,  # Default value is 1
    page_size: Annotated[int, Query(gt=0)] = 10,  # Default value is 10
) -> dict:
    """
    Returns all borrowed objects. Only accessible by librarian
    """

    logging.info(f"Librarian {librarian['id']} requested all borrowed.")

    starting_index = (page_number - 1) * page_size
    borrowed = (
        db.scalars(
            select(Borrowed)
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
        data=borrowed,
    )

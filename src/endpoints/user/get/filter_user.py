import logging
from typing import Annotated, List

from fastapi import Depends, Query
from sqlalchemy.orm import Session
from starlette import status

from src.dependencies import get_current_librarian, get_db
from src.endpoints.user.exceptions import db_not_available
from src.endpoints.user.router_init import router
from src.models.user import User
from src.responses import custom_response


@router.get("", status_code=status.HTTP_200_OK, response_model=None)
async def filter_user(
    email: str | None = None,
    username: str | None = None,
    first_name: str | None = None,
    last_name: str | None = None,
    contact_number: str | None = None,
    address: str | None = None,
    page_number: Annotated[int, Query(gt=0)] = 1,  # Default value is 1
    page_size: Annotated[int, Query(gt=0)] = 10,  # Default value is 10
    librarian: dict = Depends(get_current_librarian),
    db: Session = Depends(get_db),
) -> dict:
    """
    Filters the users list based on param provided. If None given then it will
    return the complete list.
    """
    params = {
        "email": email,
        "username": username,
        "first_name": first_name,
        "last_name": last_name,
        "contact_number": contact_number,
        "address": address,
    }
    filters = {key: value for key, value in params.items() if value}
    # Adding a condition that only allow non deleted users.
    filters["is_deleted"] = False
    try:
        starting_index = (page_number - 1) * page_size
        users = (
            db.query(User)
            .filter_by(**filters)
            .offset(starting_index)
            .limit(page_size)
            .all()
        )
        return custom_response(
            status_code=status.HTTP_200_OK, details="Users found", data=users
        )
    except Exception:
        logging.exception(f"Exception occured -- {__name__}.filter_user")
        raise db_not_available()

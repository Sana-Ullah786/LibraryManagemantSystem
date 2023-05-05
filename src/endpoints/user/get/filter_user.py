import logging
from typing import List

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from src.dependencies import get_current_librarian, get_current_user, get_db
from src.endpoints.user.exceptions import db_not_available
from src.endpoints.user.router_init import router
from src.models.user import User


@router.get("", status_code=status.HTTP_200_OK, response_model=None)
async def filter_user(
    email: str | None = None,
    username: str | None = None,
    first_name: str | None = None,
    last_name: str | None = None,
    contact_number: str | None = None,
    address: str | None = None,
    librarian: dict = Depends(get_current_librarian),
    db: Session = Depends(get_db),
) -> List[User]:
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
    try:
        users = db.query(User).filter_by(**filters).all()
        return users
    except Exception:
        logging.exception(f"Exception occured -- {__name__}.filter_user")
        raise db_not_available()

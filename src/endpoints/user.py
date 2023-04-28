import logging
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette import status

from ..models.database import get_db
from ..models.user import User
from .auth import get_current_librarian

router = APIRouter(
    prefix="/user", tags=["user"], responses={401: {"user": "Not authorized"}}
)


@router.get("/", status_code=status.HTTP_200_OK, response_model=None)
def get_all_user(
    librarian: dict = Depends(get_current_librarian), db: Session = Depends(get_db)
) -> List[User]:
    """
    Returns the list of all the users registered in a library.
    Param
    -----
    JWT token of a librarian.
    Throws an exception if JWT is not of librarian
    """
    try:
        users = db.execute(select(User).where(True)).scalars().all()
        logging.info(f"Returning all users. -- {__name__}.get_all_user")
        return users
    except Exception:
        logging.exception(f"Exception occured -- {__name__}.get_all_user")
        raise db_not_available()


# Exceptions


def db_not_available() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Database is down. Try again later.",
    )

import logging
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Path
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
    Throws an exception if JWT is not of librarian\n
    Returns
    ------
    List of users: List[User]
    """
    try:
        users = db.execute(select(User).where(True)).scalars().all()
        logging.info(f"Returning all users. -- {__name__}.get_all_user")
        return users
    except Exception:
        logging.exception(f"Exception occured -- {__name__}.get_all_user")
        raise db_not_available()


@router.get("/{user_id}", status_code=status.HTTP_200_OK, response_model=None)
def get_user_by_id(
    librarian: dict = Depends(get_current_librarian),
    db: Session = Depends(get_db),
    user_id: int = Path(gt=0),
) -> User:
    """
    Returns a single user.\n
    Param
    -----
    user_id: int\n
    JWT token of a librarian.
    Throws an exception if JWT is not of librarian\n
    Returns
    ------
    user: User
    """
    try:
        user = db.execute(select(User).where(User.id == user_id)).scalars().first()
    except Exception:
        logging.exception(f"Exception occured -- {__name__}.get_user_by_id")
        raise db_not_available()
    logging.info(f"Returning a single user. -- {__name__}.get_user_by_id")
    if user:
        return user
    else:
        raise user_not_exist()


# Exceptions


def db_not_available() -> HTTPException:
    """
    Custom exception that can be raised if query execution fails.\n
    Returns
    -------
    Custom HTTPException object
    """
    return HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Database is down. Try again later.",
    )


def user_not_exist() -> HTTPException:
    """
    Custom exception that can be raised user does not exist.\n
    Returns
    -------
    Custom HTTPException object
    """
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="No such user exists",
    )

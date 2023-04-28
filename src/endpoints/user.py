import logging
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy import delete, select
from sqlalchemy.orm import Session
from starlette import status

from ..models.database import get_db
from ..models.user import User
from ..schemas.user import UserSchema
from .auth import get_current_librarian, get_current_user, get_password_hash

router = APIRouter(
    prefix="/user", tags=["user"], responses={401: {"user": "Not authorized"}}
)


@router.get("/", status_code=status.HTTP_200_OK, response_model=None)
def get_all_users(
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
    if user:
        logging.info(f"Returning a single user. -- {__name__}.get_user_by_id")
        return user
    else:
        logging.error(f"User not found -- {__name__}.get_user_by_id")
        raise user_not_exist()


@router.delete("/delete_user", status_code=status.HTTP_204_NO_CONTENT)
def delete_current_user(
    user: dict = Depends(get_current_user), db: Session = Depends(get_db)
) -> None:
    """
    Deletes the current logged in user.\n
    Params
    ------
    Requires user to be logged in using JWT.\n
    Returns
    ------
    HTTP_STATUS_CODE_204
    """
    try:
        db.execute(delete(User).where(User.id == user.get("id")))
        logging.info(
            f"Deleting user {user.get('username')} -- {__name__}.delete_current_user"
        )
        db.commit()
    except Exception:
        logging.exception(f"Exception occured -- {__name__}.delete_current_user")
        raise db_not_available()


@router.delete("/delete_user/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_by_id(
    librarian: dict = Depends(get_current_librarian),
    db: Session = Depends(get_db),
    user_id: int = Path(gt=0),
) -> None:
    """
    Deletes the user provided by id.\n
    Params
    ------
    Requires user to be logged in using JWT of librarian.\n
    Returns
    ------
    HTTP_STATUS_CODE_204
    """
    try:
        if db.execute(delete(User).where(User.id == user_id)).rowcount > 0:
            logging.info(f"Deleting user {user_id} -- {__name__}.delete_user_by_id")
            db.commit()
        else:
            logging.error("User not found -- {__name__}.delete_user_by_id")
            raise user_not_exist()
    except HTTPException:
        raise user_not_exist()
    except Exception:
        logging.exception(f"Exception occured -- {__name__}.delete_current_user")
        raise db_not_available()


@router.put("/update_user", status_code=status.HTTP_200_OK, response_model=None)
def update_current_user(
    new_user: UserSchema,
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> UserSchema:
    try:
        current_user = db.scalar(select(User).where(User.id == user.get("id")))
        current_user.email = new_user.email
        current_user.username = new_user.username
        current_user.password = get_password_hash(new_user.password)
        current_user.first_name = new_user.first_name
        current_user.last_name = new_user.last_name
        current_user.contact_number = new_user.contact_number
        current_user.address = new_user.address
        logging.info(
            f"Updating user {user.get('username')} -- {__name__}.udpate_current_user"
        )
        db.commit()
        new_user.id = current_user.id
        return new_user
    except Exception:
        logging.exception(f"Exception occured -- {__name__}.update_current_user")
        raise invalid_data()


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


def invalid_data() -> HTTPException:
    """
    Custom exception that can be raised while updating user\n
    non unique email/username is provided.
    """
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="username/email not unique",
    )

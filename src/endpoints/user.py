import logging
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy import delete, select
from sqlalchemy.orm import Session
from starlette import status

from ..models.database import get_db
from ..models.user import User
from ..schemas.update_user import UpdateUserSchema
from ..schemas.user import UserSchema

from .auth import (  # isort: skip
    get_current_librarian,  # isort: skip
    get_current_user,  # isort: skip
    get_password_hash,  # isort: skip
    verify_password,  # isort: skip
)  # isort: skip

router = APIRouter(
    prefix="/user", tags=["user"], responses={401: {"user": "Not authorized"}}
)


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
) -> None:
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


@router.get("/{user_id}", status_code=status.HTTP_200_OK, response_model=None)
async def get_user_by_id(
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


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_current_user(
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


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_by_id(
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


@router.put("/", status_code=status.HTTP_200_OK, response_model=None)
async def update_current_user(
    new_user: UpdateUserSchema,
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> UpdateUserSchema:
    """
    Updates the current logged in user.\n
    Params
    ------
    Requires user to be logged in using JWT\n
    Returns
    ------
    HTTP_STATUS_CODE_200
    """
    try:
        current_user = db.scalar(select(User).where(User.id == user.get("id")))
        if not verify_password(new_user.old_password, current_user.password):
            raise old_pass_not_matched()
        return update_user(new_user, user.get("id"), db)
    except HTTPException:
        raise old_pass_not_matched()
    except Exception:
        logging.exception(f"Exception occured -- {__name__}.update_current_user")
        raise invalid_data()


@router.put("/{user_id}", status_code=status.HTTP_200_OK, response_model=None)
async def update_current_user_by_id(
    new_user: UpdateUserSchema,
    user_id: int = Path(gt=0),
    librarian: dict = Depends(get_current_librarian),
    db: Session = Depends(get_db),
) -> UpdateUserSchema:
    """
    Updates the user whose id is given\n
    Params
    ------
    Requires user to be logged in using JWT as librarian\n
    Returns
    ------
    HTTP_STATUS_CODE_200
    """
    try:
        current_lib = db.scalar(select(User).where(User.id == librarian.get("id")))
        if not verify_password(new_user.old_password, current_lib.password):
            raise old_pass_not_matched()
        return update_user(new_user, user_id, db)
    except HTTPException as e:
        if e.status_code == status.HTTP_401_UNAUTHORIZED:
            raise old_pass_not_matched()
        elif e.status_code == status.HTTP_404_NOT_FOUND:
            raise user_not_exist()
    except Exception:
        logging.exception(f"Exception occured -- {__name__}.update_current_user")
        raise invalid_data()


# Exceptions


def update_user(
    new_user: UpdateUserSchema, user_id: int, db: Session
) -> UpdateUserSchema:
    """
    Updates the db with new user data.\n
    Params
    ------
    new_user: New user data
    user_id: int id of the user to update the data of.
    """
    current_user = db.scalar(select(User).where(User.id == user_id))
    if not current_user:
        raise user_not_exist()
    current_user.email = new_user.email
    current_user.username = new_user.username
    current_user.password = get_password_hash(new_user.password)
    current_user.first_name = new_user.first_name
    current_user.last_name = new_user.last_name
    current_user.contact_number = new_user.contact_number
    current_user.address = new_user.address
    logging.info(f"Updating user {user_id} -- {__name__}.udpate_current_user")
    db.commit()
    new_user.id = current_user.id
    return new_user


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


def old_pass_not_matched() -> HTTPException:
    """
    Custom exception that can be raised while updating user\n
    if old password didn't match current pass.
    """
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Old pass didn't matched",
    )

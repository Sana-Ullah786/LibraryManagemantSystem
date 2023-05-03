import logging

from fastapi import Depends, Path
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette import status

from ...dependencies import get_current_user, get_db
from ...models.user import User
from ..auth import get_current_librarian
from .exceptions import db_not_available, user_not_exist
from .router_init import router


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

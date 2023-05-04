import logging

from fastapi import Depends
from sqlalchemy import delete
from sqlalchemy.orm import Session
from starlette import status

from src.dependencies import get_current_user, get_db
from src.endpoints.user.exceptions import db_not_available
from src.endpoints.user.router_init import router
from src.models.user import User


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

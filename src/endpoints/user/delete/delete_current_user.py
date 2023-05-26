import logging
import os
from datetime import timedelta

from fastapi import Depends
from sqlalchemy import delete, select
from sqlalchemy.orm import Session
from starlette import status

from src.dependencies import get_current_user, get_db, redis_conn
from src.endpoints.user.router_init import router
from src.exceptions import custom_exception
from src.models.user import User

TOKEN_EXPIRE_TIME = int(os.getenv("JWT_EXPIRE_TIME_IN_MINUTES"))


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
        user_to_delete = db.scalar(select(User).where(User.id == user.get("id")))
        if user_to_delete is None:
            raise custom_exception(status.HTTP_404_NOT_FOUND, "User not found")
        user_to_delete.is_deleted = True
        db.commit()
        logging.info(
            f"Deleting user {user.get('username')} -- {__name__}.delete_current_user"
        )
        db.commit()
        # Black listing the user so if user is already logged in it wont be able to make further request.
        expire_time = timedelta(minutes=TOKEN_EXPIRE_TIME)
        redis_conn.setex(f"bl_user_{user.get('id')}", expire_time, user.get("id"))
    except Exception as e:
        logging.exception(f"Exception occured -- {__name__}.delete_current_user")
        raise custom_exception(
            status_code=status.HTTP_400_BAD_REQUEST,
            details="Error deleting user. details = " + str(e),
        )

import logging
import os
from datetime import timedelta

from fastapi import Depends, HTTPException, Path
from sqlalchemy import and_, not_, select
from sqlalchemy.orm import Session
from starlette import status

from src.dependencies import get_current_librarian, get_db, redis_conn
from src.endpoints.user.exceptions import db_not_available, user_not_exist
from src.endpoints.user.router_init import router
from src.exceptions import custom_exception
from src.models.user import User

TOKEN_EXPIRE_TIME = int(os.getenv("JWT_EXPIRE_TIME_IN_MINUTES"))


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
        user_to_delete = db.scalar(
            select(User).where(and_(User.id == user_id, not_(User.is_deleted)))
        )
        if user_to_delete is None:
            logging.error("User not found -- {__name__}.delete_user_by_id")
            raise custom_exception(status.HTTP_404_NOT_FOUND, "User not found")
        user_to_delete.is_deleted = True
        logging.info(f"Deleting user {user_id} -- {__name__}.delete_user_by_id")
        db.commit()
        # Black listing the user so if user is already logged in it wont be able to make further request.
        expire_time = timedelta(minutes=TOKEN_EXPIRE_TIME)
        redis_conn.setex(f"bl_user_{user_id}", expire_time, user_id)
    except HTTPException:
        raise custom_exception(
            status_code=status.HTTP_404_NOT_FOUND, details="User not found."
        )
    except Exception as e:
        logging.exception(f"Exception occured -- {__name__}.delete_current_user")
        raise custom_exception(
            status_code=status.HTTP_400_BAD_REQUEST,
            details="Error deleting user. details = " + str(e),
        )

import logging

from fastapi import Depends
from sqlalchemy import delete, select
from sqlalchemy.orm import Session
from starlette import status

from src.dependencies import get_current_user, get_db
from src.endpoints.user.exceptions import db_not_available
from src.endpoints.user.router_init import router
from src.models.user import User
from src.responses import custom_response


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
            raise custom_response(status.HTTP_404_NOT_FOUND, "User not found")
        user_to_delete.is_deleted = True
        db.commit()
        logging.info(
            f"Deleting user {user.get('username')} -- {__name__}.delete_current_user"
        )
        db.commit()
    except Exception:
        logging.exception(f"Exception occured -- {__name__}.delete_current_user")
        raise db_not_available()

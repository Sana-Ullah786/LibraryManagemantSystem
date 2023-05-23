import logging

from fastapi import Depends, HTTPException, Path
from sqlalchemy import delete, select
from sqlalchemy.orm import Session
from starlette import status

from src.dependencies import get_current_librarian, get_current_user, get_db
from src.endpoints.user.exceptions import db_not_available, user_not_exist
from src.endpoints.user.router_init import router
from src.exceptions import custom_exception
from src.models.user import User


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
        user_to_delete = db.scalar(select(User).where(User.id == user_id))
        if user_to_delete is None:
            logging.error("User not found -- {__name__}.delete_user_by_id")
            raise custom_exception(status.HTTP_404_NOT_FOUND, "User not found")
        user_to_delete.is_deleted = True
        logging.info(f"Deleting user {user_id} -- {__name__}.delete_user_by_id")
        db.commit()
    except HTTPException:
        raise user_not_exist()
    except Exception:
        logging.exception(f"Exception occured -- {__name__}.delete_current_user")
        raise db_not_available()

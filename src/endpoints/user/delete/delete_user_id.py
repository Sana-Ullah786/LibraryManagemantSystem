import logging

from fastapi import Depends, HTTPException, Path
from sqlalchemy import delete
from sqlalchemy.orm import Session
from starlette import status

from src.dependencies import get_current_librarian, get_current_user, get_db
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
        if db.execute(delete(User).where(User.id == user_id)).rowcount > 0:
            logging.info(f"Deleting user {user_id} -- {__name__}.delete_user_by_id")
            db.commit()
        else:
            logging.error("User not found -- {__name__}.delete_user_by_id")
            raise custom_exception(
                status_code=status.HTTP_404_NOT_FOUND, details="User not found."
            )
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

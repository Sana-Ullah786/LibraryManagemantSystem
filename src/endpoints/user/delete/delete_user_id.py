import logging

from fastapi import Depends, HTTPException, Path
from sqlalchemy import delete
from sqlalchemy.orm import Session
from starlette import status

from ....dependencies import get_current_user, get_db
from ....models.user import User
from ...auth import get_current_librarian
from ..exceptions import db_not_available, user_not_exist
from ..router_init import router


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

import logging

from fastapi import Depends, HTTPException, Path
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette import status

from src.endpoints.user.router_init import router
from src.endpoints.user.user_utils import update_user
from src.exceptions import custom_exception
from src.models.user import User
from src.schemas.update_user import UpdateUserSchema

from src.dependencies import (  # isort: skip
    get_current_librarian,  # isort: skip
    get_current_user,  # isort: skip
    get_db,  # isort: skip
    verify_password,  # isort: skip
)  # isort: skip


@router.put("/{user_id}", status_code=status.HTTP_200_OK, response_model=None)
async def update_current_user_by_id(
    new_user: UpdateUserSchema,
    user_id: int = Path(gt=0),
    librarian: dict = Depends(get_current_librarian),
    db: Session = Depends(get_db),
) -> dict:
    """
    Updates the user whose id is given\n
    Params
    ------
    Requires user to be logged in using JWT as librarian\n
    Returns
    ------
    dict : A dict with status code, details and data
    """
    try:
        current_lib = db.scalar(select(User).where(User.id == librarian.get("id")))
        if not verify_password(new_user.old_password, current_lib.password):
            raise custom_exception(
                status_code=status.HTTP_401_UNAUTHORIZED,
                details="Old password not matched.",
            )
        return update_user(new_user, user_id, db)
    except HTTPException as e:
        if e.status_code == status.HTTP_401_UNAUTHORIZED:
            raise custom_exception(
                status_code=status.HTTP_401_UNAUTHORIZED,
                details="Old password not matched.",
            )
        elif e.status_code == status.HTTP_404_NOT_FOUND:
            raise custom_exception(
                status_code=status.HTTP_404_NOT_FOUND, details="User not found."
            )
    except Exception as exp:
        logging.exception(f"Exception occured -- {__name__}.update_current_user")
        raise custom_exception(
            status_code=status.HTTP_400_BAD_REQUEST,
            details="Error updating user. details = " + str(exp),
        )

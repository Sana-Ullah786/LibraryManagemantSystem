import logging

from fastapi import Depends, HTTPException, Path
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette import status

from src.dependencies import get_current_user, get_db, verify_password
from src.endpoints.user.exceptions import invalid_data, old_pass_not_matched
from src.endpoints.user.router_init import router
from src.endpoints.user.user_utils import update_user
from src.models.user import User
from src.schemas.update_user import UpdateUserSchema


@router.put("/", status_code=status.HTTP_200_OK, response_model=None)
async def update_current_user(
    new_user: UpdateUserSchema,
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict:
    """
    Updates the current logged in user.\n
    Params
    ------
    Requires user to be logged in using JWT\n
    Returns
    ------
    dict : A dict with status code, details and data
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

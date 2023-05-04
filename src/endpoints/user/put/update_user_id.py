import logging

from fastapi import Depends, HTTPException, Path
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette import status

from ....dependencies import get_current_user, get_db
from ....models.user import User
from ....schemas.update_user import UpdateUserSchema
from ...auth import get_current_librarian, verify_password
from ..exceptions import invalid_data, old_pass_not_matched, user_not_exist
from ..router_init import router
from ..user_utils import update_user


@router.put("/{user_id}", status_code=status.HTTP_200_OK, response_model=None)
async def update_current_user_by_id(
    new_user: UpdateUserSchema,
    user_id: int = Path(gt=0),
    librarian: dict = Depends(get_current_librarian),
    db: Session = Depends(get_db),
) -> UpdateUserSchema:
    """
    Updates the user whose id is given\n
    Params
    ------
    Requires user to be logged in using JWT as librarian\n
    Returns
    ------
    HTTP_STATUS_CODE_200
    """
    try:
        current_lib = db.scalar(select(User).where(User.id == librarian.get("id")))
        if not verify_password(new_user.old_password, current_lib.password):
            raise old_pass_not_matched()
        return update_user(new_user, user_id, db)
    except HTTPException as e:
        if e.status_code == status.HTTP_401_UNAUTHORIZED:
            raise old_pass_not_matched()
        elif e.status_code == status.HTTP_404_NOT_FOUND:
            raise user_not_exist()
    except Exception:
        logging.exception(f"Exception occured -- {__name__}.update_current_user")
        raise invalid_data()

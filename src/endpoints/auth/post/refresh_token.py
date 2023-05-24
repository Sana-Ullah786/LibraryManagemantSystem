import logging
import os

from fastapi import Depends, status
from sqlalchemy import and_, not_
from sqlalchemy.orm import Session

from src.dependencies import get_current_user, get_db
from src.endpoints.auth.auth_utils import create_token  # isort skip
from src.endpoints.auth.router_init import router
from src.exceptions import custom_exception
from src.models.user import User
from src.responses import custom_response
from src.schemas.token import TokenSchema
from src.schemas.user import UserSchemaToken

EXPIRE_TIME_IN_MINUTES = int(os.getenv("JWT_EXPIRE_TIME_IN_MINUTES"))


@router.post("/refresh_token", status_code=status.HTTP_200_OK, response_model=None)
async def refresh_access_token(
    refresh_token: TokenSchema, db: Session = Depends(get_db)
) -> dict:
    """
    Params
    ------
    refresh_token: str passed in json body.\n
    Return
    ------
    Dict have new (fresh) access token and old refresh token\n
    """
    user_dict = get_current_user(refresh_token.refresh_token)
    user = (
        db.query(User)
        .filter(and_(User.username == user_dict.get("username"), not_(User.is_deleted)))
        .first()
    )
    if user is None:
        raise custom_exception(status.HTTP_404_NOT_FOUND, "User deleted.")
    access_token = create_token(user, EXPIRE_TIME_IN_MINUTES)
    user = UserSchemaToken(
        access_token=access_token,
        refresh_token=refresh_token.refresh_token,
        **user.__dict__,
    )
    logging.info(
        f"Generated refresh token for {user_dict.get('username')} -- {__name__}"
    )
    return custom_response(
        status_code=status.HTTP_200_OK, details="Refresh successfull", data=user
    )

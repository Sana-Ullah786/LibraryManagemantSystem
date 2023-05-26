import os

from fastapi import Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.dependencies import get_db
from src.endpoints.auth.auth_utils import authenticate_user  # isort skip
from src.endpoints.auth.auth_utils import create_token  # isort skip
from src.endpoints.auth.router_init import router
from src.exceptions import custom_exception
from src.responses import custom_response
from src.schemas.user import UserSchemaToken

EXPIRE_TIME_IN_MINUTES = int(os.getenv("JWT_EXPIRE_TIME_IN_MINUTES"))
REFRESH_TOKEN_EXPIRE_TIME_IN_MINUTES = int(
    os.getenv("JWT_REFRESH_EXPIRE_TIME_IN_MINUTES")
)


@router.post("/token", status_code=status.HTTP_200_OK, response_model=None)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
) -> dict:
    """
    Logs in a user using username and password and returns the access token and the user object.
    """
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise custom_exception(
            status_code=status.HTTP_400_BAD_REQUEST, details="Invalid credentials."
        )
    access_token = create_token(user, EXPIRE_TIME_IN_MINUTES)
    refresh_token = create_token(user, REFRESH_TOKEN_EXPIRE_TIME_IN_MINUTES)
    user = UserSchemaToken(
        access_token=access_token, refresh_token=refresh_token, **user.__dict__
    )
    return custom_response(
        status_code=status.HTTP_200_OK, details="Login successful.", data=user
    )

import logging

from fastapi import Depends, status
from sqlalchemy.orm import Session

from src.dependencies import get_db
from src.endpoints.auth.auth_utils import create_user
from src.endpoints.auth.router_init import router
from src.models.user import User
from src.responses import custom_response
from src.schemas.user import UserSchemaIn, UserSchemaOut


@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=None)
async def create_new_user(user: UserSchemaIn, db: Session = Depends(get_db)) -> dict:
    """
    Creates a new user
    """
    user = create_user(user, is_librarian=False, db=db)
    logging.info(f"New User with ID {user.id} created.")
    return custom_response(
        status_code=status.HTTP_201_CREATED,
        details="User created successfully.",
        data=user,
    )

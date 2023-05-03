import os
from datetime import datetime, timedelta
from typing import Optional

import pytz
from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..dependencies import get_current_librarian  # isort skip
from ..dependencies import get_db  # isort skip
from ..dependencies import get_password_hash  # isort skip
from ..dependencies import get_token_exception  # isort skip
from ..dependencies import get_user_already_exists_exception  # isort skip
from ..dependencies import verify_password  # isort skip; isort skip
from ..models.user import User
from ..schemas.user import UserSchema

SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = os.getenv("JWT_ALGORITHM")


router = APIRouter(
    prefix="/auth", tags=["auth"], responses={401: {"user": "Not authorized"}}
)


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def create_new_user(
    user: UserSchema, db: Session = Depends(get_db)
) -> dict[str, str]:
    """
    Creates a new user
    """
    create_user(user, is_librarian=False, db=db)
    return {"status": "success", "message": "User created"}


@router.post("/librarian/register", status_code=status.HTTP_201_CREATED)
async def create_new_librarian(
    user: UserSchema,
    db: Session = Depends(get_db),
    librarian: dict = Depends(get_current_librarian),
) -> dict[str, str]:
    """
    Creates a new librarian (requires authentication by another librarian)
    """
    create_user(user, is_librarian=True, db=db)
    return {"status": "success", "message": "Librarian created"}


@router.post("/token", status_code=status.HTTP_200_OK)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
) -> dict[str, str | bool]:
    """
    Logs in a user using username and password and returns the access token and a boolean indicating whether the user is a librarian
    """
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise get_token_exception()
    token_expires = timedelta(minutes=20)
    token = create_access_token(user.username, user.id, expires_delta=token_expires)
    return {"token": token, "is_librarian": user.is_librarian}


# Helper functions

bcryp_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_user(user: UserSchema, is_librarian: bool, db: Session) -> None:
    """
    Helper function that creates a user based on the parameters provided. It also checks if the user already exists. Raises an exception if it does.
    """

    check_user_already_exists(user, db)

    new_user = User()
    new_user.email = user.email
    new_user.username = user.username
    new_user.first_name = user.first_name
    new_user.last_name = user.last_name
    new_user.password = get_password_hash(user.password)
    new_user.is_active = True
    new_user.contact_number = user.contact_number
    new_user.address = user.address
    new_user.date_of_joining = datetime.now(pytz.UTC)
    new_user.is_active = True
    new_user.is_librarian = is_librarian

    db.add(new_user)
    db.commit()


def authenticate_user(username: str, password: str, db: Session) -> User | bool:
    """A helper function that authenticates a given username and password"""

    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def create_access_token(
    username: str, user_id: int, expires_delta: Optional[timedelta] = None
) -> str:
    """
    Takes in a username, id and expire time and returns a JWT access token for the user
    """
    encode = {"sub": username, "id": user_id}
    if expires_delta:
        expire = datetime.utcnow() + timedelta(minutes=15)
    encode.update({"exp": expire})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


def check_user_already_exists(user: UserSchema, db: Session) -> None:
    """
    Raises an exception is user with the same email or username already exists
    """

    fetched_user = db.scalar(
        select(User).where(User.email == user.email or User.username == user.username)
    )
    if fetched_user:
        raise get_user_already_exists_exception()

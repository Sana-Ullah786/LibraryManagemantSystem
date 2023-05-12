import os
from datetime import datetime, timedelta

import pytz
from jose import jwt
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.dependencies import get_password_hash  # isort skip
from src.dependencies import get_user_already_exists_exception  # isort skip
from src.dependencies import verify_password  # isort skip; isort skip
from src.models.user import User
from src.schemas.user import UserSchemaIn, UserSchemaOut

SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = os.getenv("JWT_ALGORITHM")
EXPIRE_TIME_IN_MINUTES = int(os.getenv("JWT_EXPIRE_TIME_IN_MINUTES"))


def create_user(user: UserSchemaIn, is_librarian: bool, db: Session) -> UserSchemaOut:
    """
    Helper function that creates a user based on the parameters provided and returns the user. It also checks if the user already exists. Raises an exception if it does.
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
    db.refresh(new_user)
    user = UserSchemaOut(**new_user.__dict__)
    return user


def check_user_already_exists(user: UserSchemaIn, db: Session) -> None:
    """
    Raises an exception is user with the same email or username already exists
    """

    fetched_user = db.scalar(
        select(User).where(User.email == user.email or User.username == user.username)
    )
    if fetched_user:
        raise get_user_already_exists_exception()


def authenticate_user(username: str, password: str, db: Session) -> User | bool:
    """A helper function that authenticates a given username and password"""

    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def create_access_token(username: str, user_id: int) -> str:
    """
    Takes in a username and id and returns a JWT access token for the user
    """
    encode = {"sub": username, "id": user_id}
    expire = datetime.utcnow() + timedelta(minutes=EXPIRE_TIME_IN_MINUTES)
    encode.update({"exp": expire})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


def get_jwt_exp(token: str) -> int:
    """
    Returns the expiry for a given token
    """
    decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return decoded["exp"]

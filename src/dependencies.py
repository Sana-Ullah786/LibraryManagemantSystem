import logging
import os
from typing import Generator, Tuple

import redis
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.exceptions import custom_exception
from src.models.database import SessionLocal
from src.models.user import User

SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = os.getenv("JWT_ALGORITHM")
REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")

bcryp_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="token")

redis_conn = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)


def get_db() -> Generator[Session, None, None]:
    """
    A generetor function that yields the DB session
    """
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_current_user(token: str = Depends(oauth2_bearer)) -> dict:
    """
    Fetches user details for a given token.
    To be used as a dependency by authenticated routes for users
    """
    try:
        return check_blacklist_and_decode_jwt(token)
    except JWTError:
        raise custom_exception(
            status_code=status.HTTP_401_UNAUTHORIZED,
            details="Could not validate credentials for user",
            headers={"WWW-Authenticate": "Bearer"},
        )


def get_current_librarian(token: str = Depends(oauth2_bearer)) -> dict:
    """
    Verifies that user for given token is librarian and fetches details.
    To be used as a dependency by authenticated routes for librarians
    """
    try:
        user_dict = check_blacklist_and_decode_jwt(token)
        if not user_dict.get("is_librarian"):
            raise custom_exception(
                status_code=status.HTTP_401_UNAUTHORIZED,
                details="Could not validate credentials for librarian",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user_dict
    except JWTError:
        raise custom_exception(
            status_code=status.HTTP_401_UNAUTHORIZED,
            details="Could not validate credentials for librarian",
            headers={"WWW-Authenticate": "Bearer"},
        )


# Helper functions


def check_blacklist_and_decode_jwt(token: str) -> Tuple[str | None]:
    """
    Checks a given token against the redis blacklist. Raises an exception if it exists.\n
    Decodes the given jwt token and returns the sub (username) and id. Raises an exception if any of these are None
    """
    if redis_conn.get(f"bl_{token}"):
        logging.error(f"black listed token used -- {__name__}")
        raise custom_exception(
            status_code=status.HTTP_401_UNAUTHORIZED,
            details="Could not validate credentials for user",
            headers={"WWW-Authenticate": "Bearer"},
        )

    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    username = payload.get("sub")
    user_id = payload.get("id")
    # Validating if user is already blacklisted (Deleted by librarian after users loggin)
    if redis_conn.get(f"bl_user_{user_id}"):
        logging.error(f"user deleted -- {__name__}")
        raise custom_exception(
            status_code=status.HTTP_404_NOT_FOUND,
            details="User deleted",
            headers={"WWW-Authenticate": "Bearer"},
        )
    is_librarian = payload.get("is_librarian")
    if username is None or user_id is None:
        logging.error(f"invalid username or userid -- {__name__}")
        raise custom_exception(
            status_code=status.HTTP_401_UNAUTHORIZED,
            details="Could not validate credentials for user",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"username": username, "id": user_id, "is_librarian": is_librarian}


def get_password_hash(password: str) -> str:
    """A helper function that hashes a given password"""

    return bcryp_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """A helper function that verifies a given password against a hashed password"""

    return bcryp_context.verify(plain_password, hashed_password)

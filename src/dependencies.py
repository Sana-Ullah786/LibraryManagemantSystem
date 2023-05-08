import os
from typing import Generator, Tuple

import redis
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.orm import Session

from .models.database import SessionLocal
from .models.user import User

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
        username, user_id = check_blacklist_and_decode_jwt(token)
        return {"username": username, "id": user_id}
    except JWTError:
        raise get_user_exception()


def get_current_librarian(
    token: str = Depends(oauth2_bearer), db: Session = Depends(get_db)
) -> dict:
    """
    Verifies that user for given token is librarian and fetches details.
    To be used as a dependency by authenticated routes for librarians
    """
    try:
        username, user_id = check_blacklist_and_decode_jwt(token)
        user = db.scalar(select(User).where(User.id == user_id))
        if not user.is_librarian:
            raise get_librarian_exception()
        return {"username": username, "id": user_id}
    except JWTError:
        raise get_librarian_exception()


# Helper functions


def check_blacklist_and_decode_jwt(token: str) -> Tuple[str | None]:
    """
    Checks a given token against the redis blacklist. Raises an exception if it exists.\n
    Decodes the given jwt token and returns the sub (username) and id. Raises an exception if any of these are None
    """
    if redis_conn.get(f"bl_{token}"):
        raise get_user_exception()

    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    username = payload.get("sub")
    user_id = payload.get("id")
    if username is None or user_id is None:
        raise get_user_exception()
    return username, user_id


def get_password_hash(password: str) -> str:
    """A helper function that hashes a given password"""

    return bcryp_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """A helper function that verifies a given password against a hashed password"""

    return bcryp_context.verify(plain_password, hashed_password)


# Exceptions


def get_user_exception() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials for user",
        headers={"WWW-Authenticate": "Bearer"},
    )


def get_librarian_exception() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials for librarian",
        headers={"WWW-Authenticate": "Bearer"},
    )


def get_token_exception() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )


def get_user_already_exists_exception() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists"
    )

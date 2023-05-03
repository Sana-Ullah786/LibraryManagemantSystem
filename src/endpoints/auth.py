import os
from datetime import datetime, timedelta
from typing import Optional, Tuple

import pytz
import redis
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..models.author import Author
from ..models.book import Book
from ..models.database import get_db
from ..models.user import User
from ..schemas.user import UserSchema

load_dotenv()


SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = os.getenv("JWT_ALGORITHM")
REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")


redis_conn = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

bcryp_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter(
    prefix="/auth", tags=["auth"], responses={401: {"user": "Not authorized"}}
)

# Dependency functions


def get_current_user(token: str = Depends(oauth2_bearer)) -> dict:
    """
    Fetches user details for a given token.
    To be used as a dependency by authenticated routes for users
    """
    try:
        username, user_id = decode_jwt(token)
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
        username, user_id = decode_jwt(token)
        user = db.scalar(select(User).where(User.id == user_id))
        if not user.is_librarian:
            raise get_librarian_exception()
        return {"username": username, "id": user_id}
    except JWTError:
        raise get_librarian_exception()


# Endpoints


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


def get_password_hash(password: str) -> str:
    """A helper function that hashes a given password"""

    return bcryp_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """A helper function that verifies a given password against a hashed password"""

    return bcryp_context.verify(plain_password, hashed_password)


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


def decode_jwt(token: str) -> Tuple[str | None]:
    """Decodes a given jwt token and returns the sub (username) and id. Raises an exception if any of these are None"""

    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    username = payload.get("sub")
    user_id = payload.get("id")
    if username is None or user_id is None:
        raise get_user_exception()
    return username, user_id


def check_user_already_exists(user: UserSchema, db: Session) -> None:
    """
    Raises an exception is user with the same email or username already exists
    """

    fetched_user = db.scalar(
        select(User).where(User.email == user.email or User.username == user.username)
    )
    if fetched_user:
        raise get_user_already_exists_exception()


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

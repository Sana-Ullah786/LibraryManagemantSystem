from datetime import datetime
from typing import Callable

import pytz
from client import client
from sqlalchemy import delete
from sqlalchemy.orm import sessionmaker
from starlette import status

from src.endpoints.auth import get_password_hash
from src.models.all_models import User

NOT_AUTH = {"detail": "Not authenticated"}
LIB_USER = {
    "email": "user@super.com",
    "username": "super_user",
    "password": get_password_hash("12345678"),
    "first_name": "Users First name",
    "last_name": "Tahir",
    "contact_number": "users cellphone number",
    "address": "users physical address",
    "is_librarian": True,
    "is_active": True,
    "date_of_joining": datetime.now(pytz.UTC),
}
TEST_USER = {
    "email": "user1@gmail.com",
    "username": "user1",
    "password": get_password_hash("12345678"),
    "first_name": "Users First name",
    "last_name": "Users last name",
    "contact_number": "users cellphone number",
    "address": "users physical address",
    "is_librarian": False,
    "is_active": True,
    "date_of_joining": datetime.now(pytz.UTC),
}

SUPER_USER_CRED = {"username": "super_user", "password": "12345678"}
TEST_USER_CRED = {"username": "user1", "password": "12345678"}

TEST_AUTHOR = {
    "first_name": "Talha",
    "last_name": "Tahir",
    "birth_date": "2023-04-26T00:00:00",
}


def check_no_auth(url: str, client_method: Callable) -> None:
    """
    Hit the url with no token to check response\n
    Param
    -----
    url: str to fetch from
    client_method: Function methods to call with like post | get
    """
    response = client_method(url)
    assert response.json() == NOT_AUTH
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def get_fresh_token(db: sessionmaker, data) -> str:
    """
    Clears the db, create new librarian and returns its jwt token
    """
    remove_all_users(db)
    new_user = User(**LIB_USER)
    insert_user(db, new_user)
    new_user = User(**TEST_USER)
    insert_user(db, new_user)
    jwt_token = (
        client.post(
            "/auth/token",
            data=data,
        )
        .json()
        .get("token")
    )
    return jwt_token


def remove_all_users(test_db: sessionmaker) -> None:
    """
    Removes all the users from the database.
    """
    with test_db() as db:
        db.execute(delete(User).where(True))
        db.commit()


def insert_user(test_db: sessionmaker, user: User) -> None:
    """
    Creates a user in database
    """
    with test_db() as db:
        db.add(user)
        db.commit()

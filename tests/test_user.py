import logging
from datetime import datetime
from typing import Callable

import pytz
from sqlalchemy import delete, insert, select
from sqlalchemy.orm import sessionmaker
from starlette import status

from ..src.endpoints.auth import get_password_hash
from ..src.models.all_models import User
from .client import client

NOT_AUTH = {"detail": "Not authenticated"}
LIB_USER = {
    "email": "user@super.com",
    "username": "super_user",
    "password": get_password_hash("12345678"),
    "first_name": "Users First name",
    "last_name": "Users last name",
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


def test_get_all_users(test_db: sessionmaker) -> None:
    check_no_auth("/user/", client.get)
    token = get_fresh_token(test_db, SUPER_USER_CRED)
    response = client.get("/user/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 2
    assert response.json()[0].get("username") == LIB_USER.get("username")
    assert response.json()[1].get("username") == TEST_USER.get("username")


def test_get_user_by_id(test_db: sessionmaker) -> None:
    check_no_auth("/user/", client.get)
    token = get_fresh_token(test_db, SUPER_USER_CRED)
    response = client.get("/user/2", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == status.HTTP_200_OK
    assert response.json().get("username") == "user1"

    response = client.get("/user/3", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_current_user(test_db: sessionmaker) -> None:
    check_no_auth("/user/delete_user", client.delete)
    token = get_fresh_token(test_db, TEST_USER_CRED)
    response = client.delete(
        "/user/delete_user", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT

    token = get_fresh_token(test_db, SUPER_USER_CRED)
    response = client.delete(
        "/user/delete_user", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_delete_user_by_id(test_db: sessionmaker) -> None:
    check_no_auth("/user/delete_user/2", client.delete)
    token = get_fresh_token(test_db, TEST_USER_CRED)
    response = client.delete(
        "/user/delete_user/2", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    token = get_fresh_token(test_db, SUPER_USER_CRED)
    response = client.delete(
        "/user/delete_user/2", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT

    response = client.delete(
        "/user/delete_user/2", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_update_current_user(test_db: sessionmaker) -> None:
    check_no_auth("/user/update_user", client.put)
    token = get_fresh_token(test_db, TEST_USER_CRED)
    updated_user = TEST_USER.copy()
    del updated_user["date_of_joining"]
    updated_user["password"] = "12345678"
    updated_user["old_password"] = "1234567"
    response = client.put(
        "/user/update_user",
        headers={"Authorization": f"Bearer {token}"},
        json=updated_user,
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    updated_user["old_password"] = "12345678"
    updated_user["email"] = LIB_USER["email"]
    response = client.put(
        "/user/update_user",
        headers={"Authorization": f"Bearer {token}"},
        json=updated_user,
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    updated_user["email"] = "user2@gmail.com"
    response = client.put(
        "/user/update_user",
        headers={"Authorization": f"Bearer {token}"},
        json=updated_user,
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json().get("email") == "user2@gmail.com"


def test_update_user_by_id(test_db: sessionmaker) -> None:
    check_no_auth("/user/update_user/2", client.put)
    token = get_fresh_token(test_db, TEST_USER_CRED)
    updated_user = TEST_USER.copy()
    del updated_user["date_of_joining"]
    updated_user["password"] = "12345678"
    updated_user["old_password"] = "12345678"
    response = client.put(
        "/user/update_user/2",
        headers={"Authorization": f"Bearer {token}"},
        json=updated_user,
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED  # user must be lib
    token = get_fresh_token(test_db, SUPER_USER_CRED)
    updated_user["old_password"] = "1234567"
    updated_user["email"] = "user3@gmail.com"
    response = client.put(
        "/user/update_user/2",
        headers={"Authorization": f"Bearer {token}"},
        json=updated_user,
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED  # old pass not equal
    updated_user["old_password"] = "12345678"
    updated_user["email"] = "user2@gmail.com"
    response = client.put(
        "/user/update_user/6",
        headers={"Authorization": f"Bearer {token}"},
        json=updated_user,
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND  # invalid id
    response = client.put(
        "/user/update_user/2",
        headers={"Authorization": f"Bearer {token}"},
        json=updated_user,
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json().get("email") == "user2@gmail.com"  # success


# Helper functions


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

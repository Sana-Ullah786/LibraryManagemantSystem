from datetime import datetime

import pytz
from fastapi import Response, status
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker

from src.endpoints.auth.auth_utils import get_password_hash
from src.models.user import User
from tests.client import client

TEST_USER = {
    "username": "testuser",
    "email": "testuser@gmail.com",
    "first_name": "Test",
    "last_name": "User",
    "password": "abc123A_GT!",
    "contact_number": "03123421234",
    "address": "Bahria Town",
}

TEST_USER_AUTH = {"username": "testuser", "password": "abc123A_GT!"}

## Register User Tests


def test_register_user_valid(test_db: sessionmaker) -> None:
    """
    Tests a valid user registration
    """
    response = register_user(TEST_USER)
    assert response.status_code == status.HTTP_201_CREATED

    with test_db() as db:
        user = db.scalar(
            select(User).where(
                User.username == TEST_USER["username"]
                and User.email == TEST_USER["email"]
            )
        )
        assert user


def test_register_user_invalid(test_db: sessionmaker) -> None:
    """
    Tests an invalid user registration where a required field (username) is missing
    """
    new_user = TEST_USER.copy()
    new_user.pop("username")
    response = register_user(new_user)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_register_user_already_exists(test_db: sessionmaker) -> None:
    """
    Tests an invalid user registration where user already exists
    """

    register_user(TEST_USER)
    response = register_user(TEST_USER)

    assert response.status_code == status.HTTP_400_BAD_REQUEST


## Token Tests


def test_token_valid(test_db: sessionmaker) -> None:
    """
    Tests a valid user login and fetch token
    """

    register_user(TEST_USER)
    response = login(TEST_USER_AUTH)

    assert response.status_code == status.HTTP_200_OK
    data = response.json()["data"]
    assert "token" in data
    assert "is_librarian" in data


def test_token_invalid(test_db: sessionmaker) -> None:
    """
    Tests an invalid user login (incorrect username and/or password)
    """

    register_user(TEST_USER)

    new_test_user_auth = TEST_USER_AUTH.copy()
    new_test_user_auth["username"] = "an incorrect username"
    response = login(new_test_user_auth)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    new_test_user_auth = TEST_USER_AUTH.copy()
    new_test_user_auth["password"] = "an incorrect password"
    response = login(new_test_user_auth)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


## Register Librarian Tests


def test_register_librarian_valid(test_db: sessionmaker) -> None:
    """
    Tests a valid librarian registration
    """

    token = create_librarian_and_get_token(test_db)

    librarian = TEST_USER.copy()
    librarian["email"] = "librarian_og@gmail.com"
    librarian["username"] = "librarian_og"
    response = register_librarian(librarian, token)
    assert response.status_code == status.HTTP_201_CREATED

    with test_db() as db:
        librarian = db.scalar(
            select(User).where(
                User.username == TEST_USER["username"]
                and User.email == TEST_USER["email"]
            )
        )
        assert librarian


def test_register_librarian_invalid(test_db: sessionmaker) -> None:
    """
    Tests an invalid librarian registration where a required field (username) is missing
    """
    token = create_librarian_and_get_token(test_db)

    librarian = TEST_USER.copy()
    librarian["email"] = "librarian_og@gmail.com"
    librarian.pop("username")
    response = register_librarian(librarian, token)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_register_librarian_already_exists(test_db: sessionmaker) -> None:
    """
    Tests an invalid librarian registration where librarian already exists
    """

    token = create_librarian_and_get_token(test_db)

    response = register_librarian(TEST_USER, token)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_register_librarian_without_librarian_token(test_db: sessionmaker) -> None:
    """
    Tests an invalid librarian registration where token of another librarian is not provided
    """

    response = register_librarian(TEST_USER, None)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


# Test logout


def test_logout(test_db: sessionmaker) -> None:
    """
    Tests the logout functionality
    """

    # setup
    token = create_librarian_and_get_token(test_db)

    # test
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post("/auth/logout", headers=headers)

    assert response.status_code == 200
    response = register_librarian(TEST_USER, token)
    assert response.status_code == 401


# Helper functions


def register_user(user: dict) -> Response:
    """
    Hits the register user endpoint and returns the response
    """

    return client.post("/auth/register", json=user)


def login(user_auth: dict) -> Response:
    """
    Hits the login user (token) endpoint and returns the response
    """

    return client.post("/auth/token", data=user_auth)


def create_librarian_and_get_token(test_db: sessionmaker) -> str:
    """
    Creates a librarian with the test user and returns it's token
    """

    librarian = TEST_USER.copy()
    librarian["password"] = get_password_hash(librarian["password"])
    librarian = User(**librarian)
    librarian.date_of_joining = datetime.now(pytz.UTC)
    librarian.is_active = True
    librarian.is_librarian = True

    with test_db() as db:
        db.add(librarian)
        db.commit()

    response = login(TEST_USER_AUTH)
    return response.json()["data"]["token"]


def register_librarian(librarian: dict, token: str | None = None) -> Response:
    """
    Hits the register librarian endpoint and returns the response. Also sends authentication token in headers if provided
    """

    if token:
        headers = {"Authorization": f"Bearer {token}"}
    else:
        headers = None
    return client.post("/auth/librarian/register", json=librarian, headers=headers)

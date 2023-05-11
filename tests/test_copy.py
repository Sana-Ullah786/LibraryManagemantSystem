from datetime import datetime
from typing import Callable

import pytz
from sqlalchemy.orm import sessionmaker
from starlette import status

from src.dependencies import get_password_hash
from src.models import all_models
from src.models.all_models import User
from tests.client import client

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


def test_get_copy(test_db: sessionmaker) -> None:
    copy = insert_copy(test_db, isbn="qwer", language="English")
    copy2 = insert_copy(test_db, isbn="qwerty", language="Persian")

    response = client.get("/copy")
    assert response.status_code == 200
    assert response.json()[0].get("id") == copy[1].id
    assert response.json()[1].get("id") == copy2[1].id

    # get all books by book id

    response = client.get(f"/copy/book/{copy[1].id}")
    assert response.json()[0].get("id") == copy[1].id

    # get all books by book id that doesnt exist

    response = client.get("/copy/book/3")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 0

    # get copy by copy id

    response = client.get(f"/copy/{copy[1].id}")
    assert response.status_code == 200
    assert response.json().get("id") == copy[1].id

    # get copy by wrong copy id

    response = client.get("/copy/3")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json().get("detail") == "Copy not found"


def test_copy_create(test_db: sessionmaker) -> None:
    copy = insert_copy(test_db, isbn="qwer", language="English")

    check_no_auth("/book", client.post)
    token = get_fresh_token(test_db, SUPER_USER_CRED)

    payload = {"book_id": copy[0].id, "language_id": copy[2].id, "status": " Available"}

    # without authentication

    response = client.post("/copy", json=payload)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    response = client.post(
        "/copy", headers={"Authorization": f"Bearer {token}"}, json=payload
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert len(response.json()) == 2
    assert response.json().get("status") == 201
    assert response.json().get("transaction") == "succesful_response"


def test_copy_update(test_db: sessionmaker) -> None:
    # succesful Update
    copy = insert_copy(test_db, isbn="qwer", language="English")

    check_no_auth("/book", client.post)
    token = get_fresh_token(test_db, SUPER_USER_CRED)

    payload = {"book_id": copy[0].id, "language_id": copy[2].id, "status": "Reserved"}
    response = client.put(
        f"/copy/{copy[1].id}",
        headers={"Authorization": f"Bearer {token}"},
        json=payload,
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT

    # check updated status
    response = client.get(f"/copy/{copy[1].id}")
    assert response.status_code == 200
    assert response.json().get("status") == "Reserved"

    # Invalid copy id

    response = client.put(
        "/copy/3", headers={"Authorization": f"Bearer {token}"}, json=payload
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json().get("detail") == "Copy not found"


def test_copy_delete(test_db: sessionmaker):
    # success delete
    copy = insert_copy(test_db, isbn="qwer", language="English")

    token = get_fresh_token(test_db, SUPER_USER_CRED)

    response = client.delete(
        f"/copy/{copy[1].id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == status.HTTP_200_OK

    # if a book is already deleted  or invalid id

    response = client.delete(
        f"/copy/{copy[1].id}", headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json().get("detail") == "Copy not found"


def insert_copy(test_db: sessionmaker, isbn, language) -> list:
    with test_db() as db:
        # setup

        language = all_models.Language(language=language)
        book = all_models.Book(
            title="Let us C",
            description="Coding book",
            isbn=isbn,
            date_of_publication=datetime(2008, 1, 1),
            language=language,
        )
        copy = all_models.Copy(book=book, language=language, status="available")
        db.add_all([language, book, copy])
        db.flush()
        db.commit()
        return [book, copy, language]


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


def insert_user(test_db: sessionmaker, user: User) -> None:
    """
    Creates a user in database
    """
    with test_db() as db:
        db.add(user)
        db.commit()

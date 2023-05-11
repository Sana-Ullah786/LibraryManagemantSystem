from datetime import datetime
from typing import Callable

import pytz
from sqlalchemy import delete
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
    "password": get_password_hash("abc123A_GT"),
    "first_name": "Users First name",
    "last_name": "Tahir",
    "contact_number": "03122345678",
    "address": "users physical address",
    "is_librarian": True,
    "is_active": True,
    "date_of_joining": datetime.now(pytz.UTC),
}
TEST_USER = {
    "email": "user1@gmail.com",
    "username": "user1",
    "password": get_password_hash("abc123A_GT"),
    "first_name": "Users First name",
    "last_name": "Users last name",
    "contact_number": "03122345678",
    "address": "users physical address",
    "is_librarian": False,
    "is_active": True,
    "date_of_joining": datetime.now(pytz.UTC),
}

SUPER_USER_CRED = {"username": "super_user", "password": "abc123A_GT"}
TEST_USER_CRED = {"username": "user1", "password": "abc123A_GT"}

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


def insert_copy(test_db: sessionmaker, isbn: str, language: str) -> list:
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


def insert_book(test_db: sessionmaker) -> list:
    author = all_models.Author(
        first_name="Charles",
        last_name="Babbage",
        birth_date=datetime(1990, 1, 1),
        death_date=datetime(2020, 1, 1),
    )
    language = all_models.Language(language="English")
    genre = all_models.Genre(genre="Comedy")

    book = all_models.Book(
        title="Let us C",
        description="Coding book",
        isbn="ABCD1234",
        date_of_publication=datetime(2008, 1, 1),
        language=language,
    )
    book.genres.append(genre)
    book.authors.append(author)

    with test_db() as db:
        db.add_all([author, language, genre, book])
        db.commit()
        db.flush()
    return [author, language, genre, book]


def insert_author(test_db: sessionmaker) -> all_models.Author:
    author = all_models.Author(
        first_name="Charles",
        last_name="Babbage",
        birth_date=datetime(1990, 1, 1),
        death_date=datetime(2020, 1, 1),
    )
    with test_db() as db:
        db.add_all([author])
        db.commit()
        db.flush()
    return author


def insert_language(test_db: sessionmaker) -> all_models.Language:
    language = all_models.Language(language="English")

    with test_db() as db:
        db.add(language)
        db.commit()
        db.flush()
    return language


def insert_genre(test_db: sessionmaker) -> all_models.Genre:
    genre = all_models.Genre(genre="English")

    with test_db() as db:
        db.add(genre)
        db.commit()
        db.flush()
    return genre

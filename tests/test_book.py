from datetime import datetime
from typing import Callable

import pytz
from sqlalchemy import select
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


def test_get_book(test_db: sessionmaker) -> None:
    author = all_models.Author(
        first_name="Charles",
        last_name="Babbage",
        birth_date=datetime(1990, 1, 1),
        death_date=datetime(2020, 1, 1),
    )
    language = all_models.Language(language="English")
    book = all_models.Book(
        title="Let us C",
        description="Coding book",
        isbn="ABCD1234",
        date_of_publication=datetime(2008, 1, 1),
        language=language,
    )
    book.authors.append(author)

    with test_db() as db:
        db.add_all([author, language, book])
        db.commit()
        db.flush()
        # db.refresh(book)
        response = client.get("/book/")
        assert response.status_code == status.HTTP_200_OK

    book = db.scalar(select(all_models.Book).where(all_models.Book.isbn == "ABCD1234"))
    response = client.get(f"/book/{book.id}")
    assert response.status_code == status.HTTP_200_OK


def test_filter_books(test_db: sessionmaker) -> None:
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

    payload = {"author": author.id, "language": language.id, "genre": genre.id}
    response = client.get(url="/book/", params=payload)
    assert response.status_code == status.HTTP_200_OK

    # testing
    author = db.scalar(
        select(all_models.Author).where(all_models.Author.first_name == "Charles")
    )
    language = db.scalar(
        select(all_models.Language).where(all_models.Language.language == "English")
    )
    genre = db.scalar(
        select(all_models.Genre).where(all_models.Genre.genre == "Comedy")
    )
    book = db.scalar(select(all_models.Book).where(all_models.Book.isbn == "ABCD1234"))
    assert response.status_code == status.HTTP_200_OK
    assert author in book.authors
    assert language == book.language
    assert book in author.books
    assert genre in book.genres

    # If no book is present for the given filters

    payload = {"author": 2, "language": 1, "genre": 4}
    response = client.get(url="/book", params=payload)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 3
    assert response.json().get("status_code") == 404
    assert response.json().get("detail") == "Book not found"


def test_book_create(test_db: sessionmaker) -> None:
    check_no_auth("/book", client.post)
    language = insert_language(test_db)
    genre = insert_genre(test_db)
    author = insert_author(test_db)
    token = get_fresh_token(test_db, SUPER_USER_CRED)

    payload = {
        "title": "TESTBook",
        "isbn": "dsasadaa135",
        "date_of_publication": "12-12-2012",
        "description": "Short dics about book, max 200 characters",
        "language_id": language.id,
        "author_ids": [author.id],
        "genre_ids": [genre.id],
    }

    response = client.post(
        "/book", headers={"Authorization": f"Bearer {token}"}, json=payload
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert len(response.json()) == 2
    assert response.json().get("status") == 201
    assert response.json().get("transaction") == "succesful_response"


def test_book_update(test_db: sessionmaker) -> None:
    check_no_auth("/book", client.post)
    book = insert_book(test_db)
    genre = insert_genre(test_db)
    author = insert_author(test_db)
    token = get_fresh_token(test_db, SUPER_USER_CRED)
    with test_db() as db:
        book = db.scalar(
            select(all_models.Book).where(all_models.Book.isbn == "ABCD1234")
        )
    payload = {
        "title": "TESTBook",
        "isbn": "dsasadaa135",
        "date_of_publication": "12-12-2012",
        "description": "Hello",
        "language_id": book.language_id,
        "author_ids": [author.id],
        "genre_ids": [genre.id],
    }

    response = client.put(
        f"/book/{book.id}", headers={"Authorization": f"Bearer {token}"}, json=payload
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json().get("description") == "Hello"


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

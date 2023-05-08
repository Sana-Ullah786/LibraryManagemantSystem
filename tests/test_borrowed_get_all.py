from datetime import datetime, timedelta

from fastapi import Response, status
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker

from src.models import all_models
from tests.client import client
from tests.test_auth import TEST_USER  # isort skip
from tests.test_auth import TEST_USER_AUTH  # isort skip
from tests.test_auth import create_librarian_and_get_token  # isort skip
from tests.test_auth import login  # isort skip
from tests.test_auth import register_user  # isort skip; isort skip


def test_borrowed_get_all(test_db: sessionmaker) -> None:
    """
    Tests the get all borrowed endpoint
    """

    token = create_librarian_and_get_token(test_db)

    # test empty
    response = make_request(token)
    data = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert data == []

    # test with entry
    borrowed = create_borrowed(test_db)
    response = make_request(token)
    data = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert len(data) == 1
    assert data[0]["user"]["email"] == borrowed.user.email
    assert data[0]["copy"]["book"]["title"] == borrowed.copy.book.title


def test_borrowed_get_all_without_token(test_db: sessionmaker) -> None:
    """
    Tests the get all borrowed endpoint with no token provided. Should return 401
    """
    response = make_request()
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_borrowed_get_all_with_user_token(test_db: sessionmaker) -> None:
    """
    Tests the get all borrowed endpoint with a user token provided. Should return 401
    """
    register_user(TEST_USER)
    token = login(TEST_USER_AUTH).json()["token"]

    response = make_request(token)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


# Helper function


def make_request(token: str | None = None) -> Response:
    """
    Helper function to make the get all borrowed request
    """

    if token:
        headers = {"Authorization": f"Bearer {token}"}
    else:
        headers = None
    return client.get("/borrowed/", headers=headers)


def create_borrowed(test_db: sessionmaker) -> all_models.Borrowed:
    """
    Helper function to create a borrowed object and save to db
    """

    with test_db() as db:
        register_user(TEST_USER)
        language = all_models.Language(language="English")
        genre = all_models.Genre(genre="Fantasy")
        author = all_models.Author(
            first_name="J.K.",
            last_name="Rowling",
            birth_date=datetime(1980, 1, 1),
            death_date=None,
        )
        book = all_models.Book(
            title="Harry Potter",
            description="The boy who lived",
            language=language,
            date_of_publication=datetime(2000, 1, 1),
            isbn="ABCD-1234",
        )
        book.authors.append(author)
        book.genres.append(genre)
        copy = all_models.Copy(book=book, language=language, status="available")
        user = db.scalar(
            select(all_models.User).where(all_models.User.email == TEST_USER["email"])
        )
        borrowed = all_models.Borrowed(
            copy=copy,
            user=user,
            issue_date=datetime.now(),
            due_date=datetime.now() + timedelta(days=2),
            return_date=None,
        )

        db.add_all([language, genre, author, book, copy, borrowed])
        db.commit()
        return borrowed

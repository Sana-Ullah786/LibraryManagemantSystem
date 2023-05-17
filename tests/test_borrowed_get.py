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
    response = make_request("/borrowed/", token)
    data = response.json()["data"]
    assert response.status_code == status.HTTP_200_OK
    assert data == []

    # test with entry
    borrowed = create_borrowed(test_db)
    response = make_request("/borrowed/", token)
    data = response.json()["data"]
    assert response.status_code == status.HTTP_200_OK
    assert len(data) == 1
    assert data[0]["user"]["email"] == borrowed.user.email
    assert data[0]["copy"]["book"]["title"] == borrowed.copy.book.title


def test_borrowed_get_all_without_token(test_db: sessionmaker) -> None:
    """
    Tests the get all borrowed endpoint with no token provided. Should return 401
    """
    response = make_request("/borrowed/")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_borrowed_get_all_with_user_token(test_db: sessionmaker) -> None:
    """
    Tests the get all borrowed endpoint with a user token provided. Should return 401
    """
    register_user(TEST_USER)
    token = login(TEST_USER_AUTH).json()["data"]["token"]

    response = make_request("/borrowed/", token)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_borrowed_get_by_id(test_db: sessionmaker) -> None:
    """
    Tests the get borrowed by id endpoint
    """

    borrowed = create_borrowed(test_db)
    token = login(TEST_USER_AUTH).json()["data"]["token"]

    response = make_request(f"/borrowed/{borrowed.id}", token)
    data = response.json()["data"]
    assert response.status_code == status.HTTP_200_OK
    assert "copy_id" in data and data["copy_id"] == borrowed.copy_id
    assert "user_id" in data and data["user_id"] == borrowed.user_id
    assert "due_date" in data and data["due_date"] == borrowed.due_date.isoformat()
    assert (
        "issue_date" in data and data["issue_date"] == borrowed.issue_date.isoformat()
    )


def test_borrowed_get_by_id_without_token(test_db: sessionmaker) -> None:
    """
    Tests the get borrowed by id endpoint without a token. Should return 401
    """
    borrowed = create_borrowed(test_db)

    response = make_request(f"/borrowed/{borrowed.id}")
    response.status_code == status.HTTP_401_UNAUTHORIZED


def test_borrowed_get_by_id_with_different_user_token(test_db: sessionmaker) -> None:
    """
    Tests the get borrowed by id endpoint with token of different user and borrowed of different user. Should return 404.
    """

    borrowed = create_borrowed(test_db)
    new_user = TEST_USER.copy()
    new_user["username"] = "newuser1"
    new_user["email"] = "newuser1@gmail.com"
    register_user(new_user)
    new_user_auth = TEST_USER_AUTH.copy()
    new_user_auth["username"] = "newuser1"
    token = login(new_user_auth).json()["data"]["token"]

    response = make_request(f"/borrowed/{borrowed.id}", token)
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_borrowed_get_all_for_logged_in_user(test_db: sessionmaker) -> None:
    """
    Tests the get all borrowed for logged in user endpoint.
    """

    borrowed = create_borrowed(test_db)
    token = login(TEST_USER_AUTH).json()["data"]["token"]

    response = make_request("/borrowed/user", token)
    data = response.json()["data"]
    assert response.status_code == status.HTTP_200_OK
    assert len(data) == 1
    assert "copy_id" in data[0] and data[0]["copy_id"] == borrowed.copy_id
    assert "user_id" in data[0] and data[0]["user_id"] == borrowed.user_id
    assert (
        "due_date" in data[0] and data[0]["due_date"] == borrowed.due_date.isoformat()
    )
    assert (
        "issue_date" in data[0]
        and data[0]["issue_date"] == borrowed.issue_date.isoformat()
    )


def test_borrowed_get_all_for_logged_in_user2(test_db: sessionmaker) -> None:
    """
    Tests the get all borrowed for logged in user endpoint by verifying that a borrowed object created by one user is not returned for another user
    """

    create_borrowed(test_db)
    new_user = TEST_USER.copy()
    new_user["username"] = "newuser1"
    new_user["email"] = "newuser1@gmail.com"
    register_user(new_user)
    new_user_auth = TEST_USER_AUTH.copy()
    new_user_auth["username"] = "newuser1"
    token = login(new_user_auth).json()["data"]["token"]

    response = make_request("/borrowed/user", token)
    data = response.json()["data"]
    assert response.status_code == status.HTTP_200_OK
    assert data == []


def test_borrowed_get_all_for_logged_in_user_without_token(
    test_db: sessionmaker,
) -> None:
    """
    Tests the get all borrowed for logged in user endpoint by requesting without a token. Should return 401.
    """

    response = make_request("/borrowed/user")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_borrowed_get_all_for_any_user(test_db: sessionmaker) -> None:
    """
    Tests the get all borrowed for any user endpoint.
    """

    user = TEST_USER.copy()
    user["email"] = "anewuser@gmail.com"
    user["username"] = "anewuser"
    borrowed = create_borrowed(test_db, user)
    token = create_librarian_and_get_token(test_db)

    response = make_request(f"/borrowed/user/{borrowed.user_id}", token)
    data = response.json()["data"]
    assert response.status_code == status.HTTP_200_OK
    assert len(data) == 1
    assert "copy_id" in data[0] and data[0]["copy_id"] == borrowed.copy_id
    assert "user_id" in data[0] and data[0]["user_id"] == borrowed.user_id
    assert (
        "due_date" in data[0] and data[0]["due_date"] == borrowed.due_date.isoformat()
    )
    assert (
        "issue_date" in data[0]
        and data[0]["issue_date"] == borrowed.issue_date.isoformat()
    )


def test_borrowed_get_all_for_any_user_with_user_token(test_db: sessionmaker) -> None:
    """
    Tests the get all borrowed for any user endpoint with a user token. Should return 401.
    """

    user_id = register_user(TEST_USER).json()["data"]["id"]
    token = login(TEST_USER_AUTH).json()["data"]["token"]

    response = make_request(f"/borrowed/user/{user_id}", token)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_borrowed_get_all_for_any_user_without_token(test_db: sessionmaker) -> None:
    """
    Tests the get all borrowed for any user endpoint without a token. Should return 401.
    """

    response = make_request("/borrowed/user/1")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


# Helper function


def make_request(endpoint: str, token: str | None = None) -> Response:
    """
    Helper function to make a request
    """

    if token:
        headers = {"Authorization": f"Bearer {token}"}
    else:
        headers = None
    return client.get(endpoint, headers=headers)


def create_borrowed(
    test_db: sessionmaker, user_dict: dict | None = None
) -> all_models.Borrowed:
    """
    Helper function to create a borrowed object and save to db
    """

    with test_db() as db:
        status = all_models.Status(status="Available")

        if not user_dict:
            user_dict = TEST_USER

        register_user(user_dict)
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
        copy = all_models.Copy(book=book, language=language, status=status)
        user = db.scalar(
            select(all_models.User).where(all_models.User.email == user_dict["email"])
        )
        borrowed = all_models.Borrowed(
            copy=copy,
            user=user,
            issue_date=datetime.now(),
            due_date=datetime.now() + timedelta(days=2),
            return_date=None,
        )

        db.add_all([status, language, genre, author, book, copy, borrowed])
        db.commit()
        return borrowed

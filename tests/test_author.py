from sqlalchemy import delete
from sqlalchemy.orm import sessionmaker
from starlette import status

from src.models.all_models import Author
from tests.client import client

# fmt: off
from tests.utils import (
    SUPER_USER_CRED,
    TEST_AUTHOR,
    TEST_USER_CRED,
    check_no_auth,
    get_fresh_token,
)

# fmt: on


def test_create_author(test_db: sessionmaker) -> None:
    delete_all_authors(test_db)
    check_no_auth("/author/", client.post)
    token = get_fresh_token(test_db, SUPER_USER_CRED)
    response = client.post(
        "/author/", headers={"Authorization": f"Bearer {token}"}, json=TEST_AUTHOR
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json().get("first_name") == TEST_AUTHOR.get("first_name")


def test_get_all_authors(test_db: sessionmaker) -> None:
    check_no_auth("/author/", client.get)
    delete_all_authors(test_db)
    # Inserting dummy data of 2 authors
    token = get_fresh_token(test_db, SUPER_USER_CRED)
    response = client.post(
        "/author/", headers={"Authorization": f"Bearer {token}"}, json=TEST_AUTHOR
    )
    SECOND_AUTHOR = TEST_AUTHOR.copy()
    SECOND_AUTHOR["first_name"] = "Tahir"
    response = client.post(
        "/author/", headers={"Authorization": f"Bearer {token}"}, json=SECOND_AUTHOR
    )

    token = get_fresh_token(test_db, TEST_USER_CRED)
    response = client.get("/author/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 2
    assert response.json()[1].get("first_name") == SECOND_AUTHOR.get("first_name")


def test_get_authors_by_id(test_db: sessionmaker) -> None:
    check_no_auth("/author/1", client.get)
    delete_all_authors(test_db)
    # Inserting dummy data of 2 authors
    token = get_fresh_token(test_db, SUPER_USER_CRED)
    response = client.post(
        "/author/", headers={"Authorization": f"Bearer {token}"}, json=TEST_AUTHOR
    )
    SECOND_AUTHOR = TEST_AUTHOR.copy()
    SECOND_AUTHOR["first_name"] = "Tahir"
    response = client.post(
        "/author/", headers={"Authorization": f"Bearer {token}"}, json=SECOND_AUTHOR
    )

    token = get_fresh_token(test_db, TEST_USER_CRED)
    response = client.get("/author/1", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == status.HTTP_200_OK
    assert response.json().get("first_name") == TEST_AUTHOR.get("first_name")
    response = client.get("/author/2", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == status.HTTP_200_OK
    assert response.json().get("first_name") == SECOND_AUTHOR.get("first_name")
    # No such author exsist
    response = client.get("/author/4", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_author_by_id(test_db: sessionmaker) -> None:
    check_no_auth("/author/1", client.delete)
    delete_all_authors(test_db)
    token = get_fresh_token(test_db, SUPER_USER_CRED)
    response = client.post(
        "/author/", headers={"Authorization": f"Bearer {token}"}, json=TEST_AUTHOR
    )
    # If user is not librarian
    token = get_fresh_token(test_db, TEST_USER_CRED)
    response = client.delete("/author/1", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    # success
    token = get_fresh_token(test_db, SUPER_USER_CRED)
    response = client.delete("/author/1", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == status.HTTP_204_NO_CONTENT
    # if no author is found of that id
    response = client.delete("/author/1", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_update_author(test_db: sessionmaker) -> None:
    check_no_auth("/author/1", client.put)
    delete_all_authors(test_db)
    # adding a dummy author
    token = get_fresh_token(test_db, SUPER_USER_CRED)
    response = client.post(
        "/author/", headers={"Authorization": f"Bearer {token}"}, json=TEST_AUTHOR
    )

    # If user is not librarian
    token = get_fresh_token(test_db, TEST_USER_CRED)
    response = client.put("/author/1", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    # success
    token = get_fresh_token(test_db, SUPER_USER_CRED)
    SECOND_AUTHOR = TEST_AUTHOR.copy()
    SECOND_AUTHOR["first_name"] = "Tahir"
    response = client.put(
        "/author/1", headers={"Authorization": f"Bearer {token}"}, json=SECOND_AUTHOR
    )
    assert response.status_code == status.HTTP_200_OK
    response = client.get("/author/1", headers={"Authorization": f"Bearer {token}"})
    assert response.json().get("first_name") == SECOND_AUTHOR.get("first_name")
    # if no author is found of that id
    response = client.put(
        "/author/3", headers={"Authorization": f"Bearer {token}"}, json=SECOND_AUTHOR
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


def delete_all_authors(test_db: sessionmaker) -> None:
    """
    Helper function that can be used to delete all authors
    """
    with test_db() as db:
        db.execute(delete(Author).where(True))
        db.commit()

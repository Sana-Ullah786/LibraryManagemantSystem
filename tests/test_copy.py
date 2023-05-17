from sqlalchemy.orm import sessionmaker
from starlette import status

from src.dependencies import get_password_hash
from src.models import all_models
from src.models.all_models import User
from tests.client import client
from tests.utils import SUPER_USER_CRED  # isort skip
from tests.utils import check_no_auth  # isort skip
from tests.utils import get_fresh_token  # isort skip
from tests.utils import insert_copy  # isort skip


def test_get_copy(test_db: sessionmaker) -> None:
    copy = insert_copy(
        test_db, isbn="qwer", language="English", status_name="available"
    )
    copy2 = insert_copy(
        test_db, isbn="qwerty", language="Persian", status_name="reserved"
    )

    response = client.get("/copy")
    assert response.status_code == 200
    assert response.json()["data"][0].get("id") == copy[1].id
    assert response.json()["data"][1].get("id") == copy2[1].id

    # get all books by book id

    response = client.get(f"/copy/book/{copy[1].id}")
    assert response.json()["data"][0].get("id") == copy[1].id

    # get all books by book id that doesnt exist

    response = client.get("/copy/book/3")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["data"]) == 0

    # get copy by copy id

    response = client.get(f"/copy/{copy[1].id}")
    assert response.status_code == 200
    assert response.json()["data"].get("id") == copy[1].id

    # get copy by wrong copy id

    response = client.get("/copy/3")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json().get("detail") == "Copy not found"


def test_copy_create(test_db: sessionmaker) -> None:
    copy = insert_copy(
        test_db, isbn="qwertiuyii", language="English", status_name="available"
    )

    check_no_auth("/book", client.post)
    token = get_fresh_token(test_db, SUPER_USER_CRED)

    payload = {"book_id": copy[0].id, "language_id": copy[2].id, "status_id": 1}

    # without authentication

    response = client.post("/copy", json=payload)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    response = client.post(
        "/copy", headers={"Authorization": f"Bearer {token}"}, json=payload
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json().get("status_code") == 201


def test_copy_update(test_db: sessionmaker) -> None:
    # succesful Update
    copy = insert_copy(
        test_db, isbn="qwertutuis", language="English", status_name="available"
    )

    check_no_auth("/book", client.post)
    token = get_fresh_token(test_db, SUPER_USER_CRED)

    payload = {"book_id": copy[0].id, "language_id": copy[2].id, "status_id": 1}
    response = client.put(
        f"/copy/{copy[1].id}",
        headers={"Authorization": f"Bearer {token}"},
        json=payload,
    )
    assert response.status_code == status.HTTP_200_OK

    # without authentication
    response = client.put("/copy", json=payload)
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    # check updated status
    response = client.get(f"/copy/{copy[1].id}")
    assert response.status_code == 200
    assert response.json()["data"].get("status") == "reserved"

    # Invalid copy id

    response = client.put(
        "/copy/3", headers={"Authorization": f"Bearer {token}"}, json=payload
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json().get("detail") == "Copy not found"


def test_copy_delete(test_db: sessionmaker):
    # success delete
    copy = insert_copy(
        test_db, isbn="qwdadsaxser", language="English", status_name="available"
    )

    token = get_fresh_token(test_db, SUPER_USER_CRED)

    response = client.delete(
        f"/copy/{copy[1].id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT

    # if a book is already deleted  or invalid id

    response = client.delete(
        f"/copy/{copy[1].id}", headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json().get("detail") == "Copy not found"

from sqlalchemy import delete
from sqlalchemy.orm import sessionmaker
from starlette import status

from ..src.models.all_models import Author
from .client import client
from .utils import SUPER_USER_CRED, TEST_AUTHOR, check_no_auth, get_fresh_token


def test_create_author(test_db: sessionmaker) -> None:
    delete_all_authors(test_db)
    check_no_auth("/author/", client.post)
    token = get_fresh_token(test_db, SUPER_USER_CRED)
    response = client.post(
        "/author/", headers={"Authorization": f"Bearer {token}"}, json=TEST_AUTHOR
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json().get("first_name") == TEST_AUTHOR.get("first_name")


def delete_all_authors(test_db: sessionmaker) -> None:
    """
    Helper function that can be used to delete all authors
    """
    with test_db() as db:
        db.execute(delete(Author).where(True))
        db.commit()

from sqlalchemy.orm import sessionmaker

from .client import client


def test_get_users(test_db: sessionmaker):
    response = client.get("/users/")
    assert response.json() == "[]"

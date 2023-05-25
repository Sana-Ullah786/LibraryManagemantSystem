import logging
from datetime import datetime

from fastapi import status

from src.models import all_models
from tests.client import client
from tests.test_language_api import create_user_using_model, get_token_for_user

# Test cases for Genre API


# Test create Genre (POST /genre/)
def test_create_genre(test_db) -> None:
    """
    This function will be used to test the create in Genre API.
    Parameters:
        test_db: The database session.
    Returns:
        None
    """
    logging.info("Testing create Genre API")
    token = None
    response = client.post(
        "/genre/", json={}, headers={"Authorization": f"Bearer {token}"}
    )
    logging.info(
        "Tested create genre API with status code: " + str(response.status_code)
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    create_user_using_model(test_db, librarian=True)
    token = get_token_for_user(test_db)
    data = {"genre": "Test"}
    response = client.post(
        "/genre/", json=data, headers={"Authorization": f"Bearer {token}"}
    )
    logging.info(
        "Tested create genre API with status code: " + str(response.status_code)
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["data"]["genre"] == "Test"
    assert response.json()["data"]["id"] == 1


# Test case for get all genre (GET /genre/)
def test_get_all_genre(test_db) -> None:
    """
    This function will be used to test the get all genre API.
    Parameters:
        test_db: The database session.
    Returns:
        None
    """
    logging.info("Testing get all genre API")
    test_create_genre(test_db)
    response = client.get("/genre/")
    logging.info(
        "Tested get all genre API with status code: " + str(response.status_code)
    )
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["data"]) == 1
    assert response.json()["data"][0]["genre"] == "Test"
    assert response.json()["data"][0]["id"] == 1


# Test case for get genre by id (GET /genre/{genre_id})
def test_get_genre_by_id(test_db) -> None:
    """
    This function will be used to test the get genre by id API.
    Parameters:
        test_db: The database session.
    Returns:
        None
    """
    logging.info("Testing get genre by id API")
    test_create_genre(test_db)
    response = client.get("/genre/1")
    logging.info(
        "Tested get genre by id API with status code: " + str(response.status_code)
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["data"]["genre"] == "Test"
    assert response.json()["data"]["id"] == 1


# Test case for update genre by id (PUT /genre/{genre_id})
def test_update_genre_by_id(test_db) -> None:
    """
    This function will be used to test the update genre by id API.
    Parameters:
        test_db: The database session.
    Returns:
        None
    """
    logging.info("Testing update genre by id API")
    test_create_genre(test_db)
    token = get_token_for_user(test_db)
    data = {"genre": "Test2"}
    # invalid id
    response = client.put(
        "/genre/2", json=data, headers={"Authorization": f"Bearer {token}"}
    )
    logging.info(
        "Tested update genre by id API with status code: " + str(response.status_code)
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    # valid id
    response = client.put(
        "/genre/1", json=data, headers={"Authorization": f"Bearer {token}"}
    )
    logging.info(
        "Tested update genre by id API with status code: " + str(response.status_code)
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["data"]["genre"] == "Test2"
    assert response.json()["data"]["id"] == 1


# Test case for delete genre by id (DELETE /genre/{genre_id})
def test_delete_genre_by_id(test_db) -> None:
    """
    This function will be used to test the delete genre by id API.
    Parameters:
        test_db: The database session.
    Returns:
        None
    """
    logging.info("Testing delete genre by id API")
    test_create_genre(test_db)
    token = get_token_for_user(test_db)
    # invalid id
    response = client.delete("/genre/-1", headers={"Authorization": f"Bearer {token}"})
    logging.info(
        "Tested delete genre by id API with status code: " + str(response.status_code)
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    # valid id
    response = client.delete("/genre/1", headers={"Authorization": f"Bearer {token}"})
    logging.info(
        "Tested delete genre by id API with status code: " + str(response.status_code)
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT
    response = client.get("/genre/")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["data"]) == 0


# Test Soft delete genre


def test_soft_delete(test_db) -> None:
    """
    This function will be used to test the soft delete genre API.
    """
    test_create_genre(test_db)
    token = get_token_for_user(test_db)
    # get all genres
    response = client.get("/genre/")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["data"]) == 1
    assert response.json()["data"][0]["genre"] == "Test"
    # soft delete language
    response = client.delete("/genre/1", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == status.HTTP_204_NO_CONTENT
    # try again to soft delete language
    response = client.delete("/genre/1", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == status.HTTP_404_NOT_FOUND
    # get all genres
    response = client.get("/genre/")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["data"]) == 0
    # update deleted genre
    data = {"genre": "Test2"}
    response = client.put(
        "/genre/1", json=data, headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    # make it un deleted
    with test_db() as db:
        language = db.query(all_models.Genre).filter(all_models.Genre.id == 1).first()
        language.is_deleted = False
        db.commit()
    # update genre
    response = client.put(
        "/genre/1", json=data, headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["data"]["genre"] == "Test2"
    assert response.json()["data"]["id"] == 1

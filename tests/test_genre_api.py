import logging
from datetime import datetime

from fastapi import status

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
    assert response.json()["genre"] == "Test"
    assert response.json()["id"] == 1


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
    assert len(response.json()) == 1
    assert response.json()[0]["genre"] == "Test"
    assert response.json()[0]["id"] == 1


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
    assert response.json()["genre"] == "Test"
    assert response.json()["id"] == 1


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
    assert response.json()["genre"] == "Test2"
    assert response.json()["id"] == 1


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
    assert len(response.json()) == 0

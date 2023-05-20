import logging

from fastapi import status

from tests.client import client
from tests.test_language_api import create_user_using_model, get_token_for_user

# Test cases for Status API


# Test create Status (POST /status/)
def test_create_status(test_db) -> None:
    """
    This function will be used to test the create in Status API.
    Parameters:
        test_db: The database session.
    Returns:
        None
    """
    logging.info("Testing create Status API")
    token = None
    response = client.post(
        "/status/", json={}, headers={"Authorization": f"Bearer {token}"}
    )
    logging.info(
        "Tested create status API with status code: " + str(response.status_code)
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    create_user_using_model(test_db, librarian=True)
    token = get_token_for_user(test_db)
    data = {"status": "Test"}
    response = client.post(
        "/status/", json=data, headers={"Authorization": f"Bearer {token}"}
    )
    logging.info(
        "Tested create status API with status code: " + str(response.status_code)
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["data"]["status"] == "Test"
    assert response.json()["data"]["status_id"] == 1


# Test case for get all status (GET /status/)
def test_get_all_status(test_db) -> None:
    """
    This function will be used to test the get all status API.
    Parameters:
        test_db: The database session.
    Returns:
        None
    """
    logging.info("Testing get all status API")
    test_create_status(test_db)
    response = client.get("/status/")
    logging.info(
        "Tested get all status API with status code: " + str(response.status_code)
    )
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["data"]) == 1
    assert response.json()["data"][0]["status"] == "Test"
    assert response.json()["data"][0]["id"] == 1


# Test case for get status by id (GET /status/{status_id})
def test_get_status_by_id(test_db) -> None:
    """
    This function will be used to test the get status by id API.
    Parameters:
        test_db: The database session.
    Returns:
        None
    """
    logging.info("Testing get status by id API")
    test_create_status(test_db)
    response = client.get("/status/1")
    logging.info(
        "Tested get status by id API with status code: " + str(response.status_code)
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["data"]["status"] == "Test"
    assert response.json()["data"]["id"] == 1


# Test case for update status by id (PUT /status/{status_id})
def test_update_status_by_id(test_db) -> None:
    """
    This function will be used to test the update status by id API.
    Parameters:
        test_db: The database session.
    Returns:
        None
    """
    logging.info("Testing update status by id API")
    test_create_status(test_db)
    token = get_token_for_user(test_db)
    data = {"status": "Test2"}
    # invalid id
    response = client.put(
        "/status/2", json=data, headers={"Authorization": f"Bearer {token}"}
    )
    logging.info(
        "Tested update status by id API with status code: " + str(response.status_code)
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    # valid id
    response = client.put(
        "/status/1", json=data, headers={"Authorization": f"Bearer {token}"}
    )
    logging.info(
        "Tested update status by id API with status code: " + str(response.status_code)
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["data"]["status"] == "Test2"
    assert response.json()["data"]["status_id"] == 1


# Test case for delete status by id (DELETE /status/{status_id})
def test_delete_status_by_id(test_db) -> None:
    """
    This function will be used to test the delete status by id API.
    Parameters:
        test_db: The database session.
    Returns:
        None
    """
    logging.info("Testing delete status by id API")
    test_create_status(test_db)
    token = get_token_for_user(test_db)
    # invalid id
    response = client.delete("/status/-1", headers={"Authorization": f"Bearer {token}"})
    logging.info(
        "Tested delete status by id API with status code: " + str(response.status_code)
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    # valid id
    response = client.delete("/status/1", headers={"Authorization": f"Bearer {token}"})
    logging.info(
        "Tested delete status by id API with status code: " + str(response.status_code)
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT
    response = client.get("/status/")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["data"]) == 0

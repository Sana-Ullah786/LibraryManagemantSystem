import logging
from datetime import datetime

from fastapi import status

from src.endpoints.auth.auth_utils import get_password_hash
from src.models import all_models
from src.models.user import User
from tests.client import client


def create_user_using_model(test_db, librarian=False) -> User:
    """
    This function will be used to create a user using model.
    Parameters:
        test_db: The database session.
        librarian: The user is librarian or not.
    Returns:
        None
    """
    logging.info("Creating user in database in Test DB")
    user = User()
    user.email = "test@test.com"
    user.username = "Test"
    user.password = get_password_hash("Test")
    user.first_name = "Test"
    user.last_name = "Test"
    user.date_of_joining = datetime.now()
    user.contact_number = "Test"
    user.address = "Test"
    user.is_librarian = librarian
    user.is_active = True
    with test_db() as db:
        db.add(user)
        db.commit()
        db.refresh(user)
    logging.info("Created user in database in Test DB with id: " + str(user.id))
    return user


def get_token_for_user(test_db) -> str:
    """
    This function will be used to get token for a user.
    Parameters:
        test_db: The database session.
    Returns:
        str: The token for the user.
    """
    logging.info(
        "Getting token for user in Test DB with username: Test and password: Test"
    )
    data = {"username": "Test", "password": "Test"}
    response = client.post("/auth/token", data=data)
    logging.info("Got token for user in Test DB with username: Test and password: Test")
    return response.json()["data"]["access_token"]


# Test cases for language API


# Test case for create language (POST /language/)
def test_create_language(test_db) -> None:
    """
    This function will be used to test the create language API.
    Parameters:
        test_db: The database session.
    Returns:
        None
    """
    logging.info("Testing create language API")
    token = None
    response = client.post(
        "/language/", json={}, headers={"Authorization": f"Bearer {token}"}
    )
    logging.info(
        "Tested create language API with status code: " + str(response.status_code)
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    create_user_using_model(test_db, librarian=True)
    token = get_token_for_user(test_db)
    data = {"language": "Test"}
    response = client.post(
        "/language/", json=data, headers={"Authorization": f"Bearer {token}"}
    )
    logging.info(
        "Tested create language API with status code: " + str(response.status_code)
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["data"]["language"] == "Test"
    assert response.json()["data"]["language_id"] == 1


# Test case for get all languages (GET /language/)
def test_get_all_languages(test_db) -> None:
    """
    This function will be used to test the get all languages API.
    Parameters:
        test_db: The database session.
    Returns:
        None
    """
    logging.info("Testing get all languages API")
    test_create_language(test_db)
    response = client.get("/language/")
    logging.info(
        "Tested get all languages API with status code: " + str(response.status_code)
    )
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["data"]) == 1
    assert response.json()["data"][0]["language"] == "Test"
    assert response.json()["data"][0]["id"] == 1


# Test case for get language by id (GET /language/{language_id})
def test_get_language_by_id(test_db) -> None:
    """
    This function will be used to test the get language by id API.
    Parameters:
        test_db: The database session.
    Returns:
        None
    """
    logging.info("Testing get language by id API")
    test_create_language(test_db)
    response = client.get("/language/1")
    logging.info(
        "Tested get language by id API with status code: " + str(response.status_code)
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["data"]["language"] == "Test"
    assert response.json()["data"]["id"] == 1


# Test case for update language by id (PUT /language/{language_id})
def test_update_language_by_id(test_db) -> None:
    """
    This function will be used to test the update language by id API.
    Parameters:
        test_db: The database session.
    Returns:
        None
    """
    logging.info("Testing update language by id API")
    test_create_language(test_db)
    token = get_token_for_user(test_db)
    data = {"language": "Test2"}
    # invalid id
    response = client.put(
        "/language/2", json=data, headers={"Authorization": f"Bearer {token}"}
    )
    logging.info(
        "Tested update language by id API with status code: "
        + str(response.status_code)
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    # valid id
    response = client.put(
        "/language/1", json=data, headers={"Authorization": f"Bearer {token}"}
    )
    logging.info(
        "Tested update language by id API with status code: "
        + str(response.status_code)
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["data"]["language"] == "Test2"
    assert response.json()["data"]["language_id"] == 1


# Test case for delete language by id (DELETE /language/{language_id})
def test_delete_language_by_id(test_db) -> None:
    """
    This function will be used to test the delete language by id API.
    Parameters:
        test_db: The database session.
    Returns:
        None
    """
    logging.info("Testing delete language by id API")
    test_create_language(test_db)
    token = get_token_for_user(test_db)
    # invalid id
    response = client.delete(
        "/language/-1", headers={"Authorization": f"Bearer {token}"}
    )
    logging.info(
        "Tested delete language by id API with status code: "
        + str(response.status_code)
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    # valid id
    response = client.delete(
        "/language/1", headers={"Authorization": f"Bearer {token}"}
    )
    logging.info(
        "Tested delete language by id API with status code: "
        + str(response.status_code)
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT
    response = client.get("/language/")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["data"]) == 0


# Test soft delete language
def test_soft_delete_language(test_db) -> None:
    """
    This function will be used to test the soft delete language API.
    Parameters:
        test_db: The database session.
    """
    test_create_language(test_db)
    token = get_token_for_user(test_db)
    # get all languages
    response = client.get("/language/")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["data"]) == 1
    assert response.json()["data"][0]["language"] == "Test"
    # soft delete language
    response = client.delete(
        "/language/1", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT
    # try again to soft delete language
    response = client.delete(
        "/language/1", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    # get all languages
    response = client.get("/language/")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["data"]) == 0
    # update deleted language
    data = {"language": "Test2"}
    response = client.put(
        "/language/1", json=data, headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    # make it un deleted
    with test_db() as db:
        language = (
            db.query(all_models.Language).filter(all_models.Language.id == 1).first()
        )
        language.is_deleted = False
        db.commit()
    # update language
    response = client.put(
        "/language/1", json=data, headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["data"]["language"] == "Test2"
    assert response.json()["data"]["language_id"] == 1

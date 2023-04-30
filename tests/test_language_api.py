from datetime import datetime

from src.endpoints.auth import get_password_hash
from src.models.language import Language
from src.models.user import User

from .client import client


def create_user_using_model(test_db, librarian=False) -> None:
    """
    This function will be used to create a user using model.
    Parameters:
        test_db: The database session.
        librarian: The user is librarian or not.
    Returns:
        None
    """
    user = User()
    user.email = "Test"
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


def get_token_for_user(test_db) -> str:
    """
    This function will be used to get token for a user.
    Parameters:
        test_db: The database session.
    Returns:
        str: The token for the user.
    """
    data = {"username": "Test", "password": "Test"}
    response = client.post("/auth/token", data=data)
    return response.json()["token"]


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
    token = None
    response = client.post(
        "/language/", json={}, headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 401
    create_user_using_model(test_db, librarian=True)
    token = get_token_for_user(test_db)
    data = {"language": "Test"}
    response = client.post(
        "/language/", json=data, headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 201


# Test case for get all languages (GET /language/)
def test_get_all_languages(test_db) -> None:
    """
    This function will be used to test the get all languages API.
    Parameters:
        test_db: The database session.
    Returns:
        None
    """
    test_create_language(test_db)
    response = client.get("/language/")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["language"] == "Test"
    assert response.json()[0]["id"] == 1


# Test case for get language by id (GET /language/{language_id})
def test_get_language_by_id(test_db) -> None:
    """
    This function will be used to test the get language by id API.
    Parameters:
        test_db: The database session.
    Returns:
        None
    """
    test_create_language(test_db)
    token = get_token_for_user(test_db)
    response = client.get("/language/1", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["language"] == "Test"
    assert response.json()["id"] == 1


# Test case for update language by id (PUT /language/{language_id})
def test_update_language_by_id(test_db) -> None:
    """
    This function will be used to test the update language by id API.
    Parameters:
        test_db: The database session.
    Returns:
        None
    """
    test_create_language(test_db)
    token = get_token_for_user(test_db)
    data = {"language": "Test2"}
    # invalid id
    response = client.put(
        "/language/2", json=data, headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 404
    # valid id
    response = client.put(
        "/language/1", json=data, headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["language"] == "Test2"
    assert response.json()["id"] == 1


# Test case for delete language by id (DELETE /language/{language_id})
def test_delete_language_by_id(test_db) -> None:
    """
    This function will be used to test the delete language by id API.
    Parameters:
        test_db: The database session.
    Returns:
        None
    """
    test_create_language(test_db)
    token = get_token_for_user(test_db)
    # invalid id
    response = client.delete(
        "/language/2", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 404
    # valid id
    response = client.delete(
        "/language/1", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["language"] == "Test"
    assert response.json()["id"] == 1
    response = client.get("/language/")
    assert response.status_code == 200
    assert len(response.json()) == 0

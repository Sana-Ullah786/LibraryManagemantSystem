from .client import client

TEST_USER = {
    "username": "testuser",
    "email": "testuser@gmail.com",
    "first_name": "Test",
    "last_name": "User",
    "password": "12345678",
    "contact_number": "+921234212345",
    "address": "Bahria Town",
}


# a dummy test to verifiy the functionality of client. Will add proper tests later


def test_create_user(test_db) -> None:
    response = client.post("/auth/register", json=TEST_USER)
    assert response.status_code == 201

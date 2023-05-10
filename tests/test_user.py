from sqlalchemy.orm import sessionmaker
from starlette import status

from tests.client import client

# fmt: off
from tests.utils import (LIB_USER, SUPER_USER_CRED, TEST_USER, TEST_USER_CRED,
                         check_no_auth, get_fresh_token)

# fmt: on


def test_get_all_users(test_db: sessionmaker) -> None:
    check_no_auth("/user", client.get)
    token = get_fresh_token(test_db, SUPER_USER_CRED)
    response = client.get("/user", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 2
    assert response.json()[0].get("username") == LIB_USER.get("username")
    assert response.json()[1].get("username") == TEST_USER.get("username")


def test_get_user_by_id(test_db: sessionmaker) -> None:
    # check_no_auth("/user/", client.get)
    token = get_fresh_token(test_db, SUPER_USER_CRED)
    response = client.get("/user/2", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == status.HTTP_200_OK
    assert response.json().get("username") == "user1"

    response = client.get("/user/3", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_current_user(test_db: sessionmaker) -> None:
    check_no_auth("/user/", client.delete)
    token = get_fresh_token(test_db, TEST_USER_CRED)
    response = client.delete("/user/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == status.HTTP_204_NO_CONTENT

    token = get_fresh_token(test_db, SUPER_USER_CRED)
    response = client.delete("/user/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_delete_user_by_id(test_db: sessionmaker) -> None:
    check_no_auth("/user/2", client.delete)
    token = get_fresh_token(test_db, TEST_USER_CRED)
    response = client.delete("/user/2", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    token = get_fresh_token(test_db, SUPER_USER_CRED)
    response = client.delete("/user/2", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == status.HTTP_204_NO_CONTENT

    response = client.delete("/user/2", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_update_current_user(test_db: sessionmaker) -> None:
    check_no_auth("/user/", client.put)
    token = get_fresh_token(test_db, TEST_USER_CRED)
    updated_user = TEST_USER.copy()
    del updated_user["date_of_joining"]
    updated_user["password"] = "12345678"
    updated_user["old_password"] = "1234567"
    response = client.put(
        "/user/",
        headers={"Authorization": f"Bearer {token}"},
        json=updated_user,
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    updated_user["old_password"] = "12345678"
    updated_user["email"] = LIB_USER["email"]
    response = client.put(
        "/user/",
        headers={"Authorization": f"Bearer {token}"},
        json=updated_user,
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    updated_user["email"] = "user2@gmail.com"
    response = client.put(
        "/user/",
        headers={"Authorization": f"Bearer {token}"},
        json=updated_user,
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json().get("email") == "user2@gmail.com"


def test_update_user_by_id(test_db: sessionmaker) -> None:
    check_no_auth("/user/2", client.put)
    token = get_fresh_token(test_db, TEST_USER_CRED)
    updated_user = TEST_USER.copy()
    del updated_user["date_of_joining"]
    updated_user["password"] = "12345678"
    updated_user["old_password"] = "12345678"
    response = client.put(
        "/user/2",
        headers={"Authorization": f"Bearer {token}"},
        json=updated_user,
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED  # user must be lib
    token = get_fresh_token(test_db, SUPER_USER_CRED)
    updated_user["old_password"] = "1234567"
    updated_user["email"] = "user3@gmail.com"
    response = client.put(
        "/user/2",
        headers={"Authorization": f"Bearer {token}"},
        json=updated_user,
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED  # old pass not equal
    updated_user["old_password"] = "12345678"
    updated_user["email"] = "user2@gmail.com"
    response = client.put(
        "/user/6",
        headers={"Authorization": f"Bearer {token}"},
        json=updated_user,
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND  # invalid id
    response = client.put(
        "/user/2",
        headers={"Authorization": f"Bearer {token}"},
        json=updated_user,
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json().get("email") == "user2@gmail.com"  # success


def test_filter_user(test_db: sessionmaker) -> None:
    check_no_auth("/user", client.get)
    url = "/user?contact_number=users%20cellphone%20number"
    token = get_fresh_token(test_db, SUPER_USER_CRED)
    response = client.get(
        url,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 2
    assert response.json()[0].get("username") == LIB_USER.get("username")
    assert response.json()[1].get("username") == TEST_USER.get("username")

    url = "/user?contact_number=users%20cellphone%20number&last_name=Tahir"
    response = client.get(
        url,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 1
    assert response.json()[0].get("username") == LIB_USER.get("username")

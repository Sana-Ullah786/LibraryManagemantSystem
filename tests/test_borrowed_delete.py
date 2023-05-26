import logging
from datetime import datetime, timedelta

from fastapi import status
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker

from src.models import all_models
from tests.client import client
from tests.test_borrowed_put import create_borrowed_entry_in_db
from tests.test_language_api import get_token_for_user


# Test to delete a borrowed by id.
def test_delete_borrowed(test_db: sessionmaker) -> None:
    """
    GIVEN a FastAPI application
    WHEN the DELETE endpoint is called with an id of an existing borrowed
    THEN it should delete the borrowed from the database.
    """
    logging.warning("Testing DELETE endpoint of /borrowed/{borrowed_id}")
    borrowed_id_1, copy_id, issue_date, due_date, _ = create_borrowed_entry_in_db(
        test_db, is_librarian=True
    )
    new_return_date = datetime.now() + timedelta(days=4)
    new_return_date = new_return_date.isoformat()
    data = {
        "copy_id": copy_id,
        "issue_date": issue_date,
        "due_date": due_date,
        "return_date": new_return_date,
    }
    token = get_token_for_user(test_db)

    # get all borrowed by user
    response = client.get(
        f"/borrowed/user/",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["data"]) == 1
    logging.info(
        "Got all borrowed by user returned borrowed = " + str(response.json()["data"])
    )

    # get borrowed by id
    response = client.get(
        f"/borrowed/{borrowed_id_1}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == status.HTTP_200_OK
    logging.info(
        "Got borrowed by id returned borrowed = " + str(response.json()["data"])
    )
    # delete the borrowed
    response = client.delete(
        f"/borrowed/{borrowed_id_1}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT
    # try again to delete the borrowed
    response = client.delete(
        f"/borrowed/{borrowed_id_1}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    # get borrowed by id
    response = client.get(
        f"/borrowed/{borrowed_id_1}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND

    # get all borrowed by user
    response = client.get(
        f"/borrowed/user/",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["data"]) == 0

    # get all borrowed
    response = client.get(
        f"/borrowed/",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == status.HTTP_200_OK
    # uodate the borrowed
    response = client.put(
        f"/borrowed/{borrowed_id_1}",
        json=data,
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    # test return borrowed
    response = client.put(
        f"/borrowed/return_borrowed_user/{borrowed_id_1}",
        headers={"Authorization": f"Bearer {token}"},
        json=data,
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND

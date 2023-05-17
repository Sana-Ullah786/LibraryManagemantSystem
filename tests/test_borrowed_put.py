import logging
from datetime import datetime, timedelta

from fastapi import status
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker

from src.models import all_models
from tests.client import client
from tests.test_borrowed_post import create_required_entries_in_db
from tests.test_language_api import create_user_using_model, get_token_for_user


def create_borrowed_entry_in_db(test_db: sessionmaker, is_librarian: bool) -> int:
    """
    This function will be used to create a borrowed entry in the database.
    Parameters:
        test_db: The database session.
    Returns:
        borrowed_id: The id of the borrowed.
    """
    logging.info("Creating new borrowed in database")
    with test_db() as db:
        user = create_user_using_model(test_db, librarian=is_librarian)
        copy_id = create_required_entries_in_db(test_db, "available")

        due_date = datetime.now() + timedelta(days=2)
        due_date = due_date.isoformat()
        issue_date = datetime.now().isoformat()
        return_date = datetime.now() + timedelta(days=5)
        return_date = return_date.isoformat()
        data = {
            "copy_id": copy_id,
            "issue_date": issue_date,
            "due_date": due_date,
            "return_date": return_date,
        }
        token = get_token_for_user(test_db)
        response = client.post(
            "/borrowed", json=data, headers={"Authorization": f"Bearer {token}"}
        )
        logging.info(
            " Response status code with Token = "
            + token
            + " "
            + str(response.status_code)
        )
        response = response.json()
        borrowed_id = response.get("id")
        return borrowed_id, copy_id, issue_date, due_date, return_date


# Test case for create borrowed (PUT /borrowed/{borrowed_id})
def test_update_with_normal_user(test_db: sessionmaker) -> None:
    """
    This function will be used to test update borrowed with id.
    Parameters:
        test_db: The database session.
    Returns:
        None
    """
    with test_db() as db:
        borrowed_id, copy_id, issue_date, _, return_date = create_borrowed_entry_in_db(
            test_db, is_librarian=False
        )
        new_due_date = datetime.now() + timedelta(days=3)
        new_due_date = new_due_date.isoformat()
        data = {
            "copy_id": copy_id,
            "issue_date": issue_date,
            "due_date": new_due_date,
            "return_date": return_date,
        }
        token = get_token_for_user(test_db)
        response = client.put(
            f"/borrowed/{borrowed_id}",
            json=data,
            headers={"Authorization": f"Bearer {token}"},
        )
        logging.info(
            " Response status code with Token = "
            + token
            + " "
            + str(response.status_code)
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


# Test case for create borrowed (PUT /borrowed/{borrowed_id})
def test_update_with_wrong_borrowed_id(test_db: sessionmaker) -> None:
    """
    This function will be used to test update borrowed with id.
    Parameters:
        test_db: The database session.
    Returns:
        None
    """
    with test_db() as db:
        borrowed_id, copy_id, issue_date, _, return_date = create_borrowed_entry_in_db(
            test_db, is_librarian=True
        )
        due_date = datetime.now() + timedelta(days=3)
        due_date = due_date.isoformat()
        data = {
            "copy_id": copy_id,
            "issue_date": issue_date,
            "due_date": due_date,
            "return_date": return_date,
        }
        token = get_token_for_user(test_db)
        response = client.put(
            f"/borrowed/{borrowed_id+1}",
            json=data,
            headers={"Authorization": f"Bearer {token}"},
        )
        logging.info(
            " Response status code with Token = "
            + token
            + " "
            + str(response.status_code)
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND


# Test case for create borrowed (PUT /borrowed/{borrowed_id})
def test_update_with_librarian_due_date(test_db: sessionmaker) -> None:
    """
    This function will be used to test update borrowed with id.
    Parameters:
        test_db: The database session.
    Returns:
        None
    """
    with test_db() as db:
        borrowed_id, copy_id, issue_date, _, return_date = create_borrowed_entry_in_db(
            test_db, is_librarian=True
        )
        new_due_date = datetime.now() + timedelta(days=3)
        new_due_date = new_due_date.isoformat()
        data = {
            "copy_id": copy_id,
            "issue_date": issue_date,
            "due_date": new_due_date,
            "return_date": return_date,
        }
        token = get_token_for_user(test_db)
        # update request
        response = client.put(
            f"/borrowed/{borrowed_id}",
            json=data,
            headers={"Authorization": f"Bearer {token}"},
        )
        logging.info(
            " Response status code with Token = "
            + token
            + " "
            + str(response.status_code)
        )
        assert response.status_code == status.HTTP_200_OK
        query = select(all_models.Borrowed).where(all_models.Borrowed.id == borrowed_id)
        updated_found_borrowed = db.scalar(query)
        updated_due_date = datetime.now() + timedelta(days=3)
        updated_found_borrowed.due_date = updated_found_borrowed.due_date.date()
        assert updated_found_borrowed.due_date == updated_due_date.date()


# Test case for create borrowed (PUT /borrowed/{borrowed_id})
def test_update_with_librarian_return_date(test_db: sessionmaker) -> None:
    """
    This function will be used to test update borrowed with id.
    Parameters:
        test_db: The database session.
    Returns:
        None
    """
    with test_db() as db:
        borrowed_id, copy_id, issue_date, due_date, _ = create_borrowed_entry_in_db(
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
        # update request
        response = client.put(
            f"/borrowed/{borrowed_id}",
            json=data,
            headers={"Authorization": f"Bearer {token}"},
        )
        logging.info(
            " Response status code with Token = "
            + token
            + " "
            + str(response.status_code)
        )
        assert response.status_code == status.HTTP_200_OK
        query = select(all_models.Borrowed).where(all_models.Borrowed.id == borrowed_id)
        updated_found_borrowed = db.scalar(query)
        updated_return_date = datetime.now() + timedelta(days=4)
        updated_found_borrowed.return_date = updated_found_borrowed.return_date.date()
        assert updated_found_borrowed.return_date == updated_return_date.date()

# Test case for create borrowed (PUT /borrowed/return_borrowed_user/{borrowed_id})
def test_return_borrowed_user_with_id(test_db: sessionmaker) -> None:
    """
    This function will be used to test return borrowed with id.
    Parameters:
        test_db: The database session.
    Returns:
        None
    """
    with test_db() as db:
        borrowed_id, copy_id, issue_date, due_date, _ = create_borrowed_entry_in_db(
            test_db, is_librarian=True
        )
        new_return_date = datetime.now()
        new_return_date = new_return_date.isoformat()
        data = {
            "copy_id": copy_id,
            "issue_date": issue_date,
            "due_date": due_date,
            "return_date": new_return_date,
        }
        token = get_token_for_user(test_db)
        # update request
        response = client.put(
            f"/borrowed/return_borrowed_user/{borrowed_id}",
            json=data,
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == status.HTTP_200_OK
        query = select(all_models.Borrowed).where(all_models.Borrowed.id == borrowed_id)
        updated_found_borrowed = db.scalar(query)
        # convert new_return_date to date its an str now
        new_return_date = datetime.strptime(new_return_date, "%Y-%m-%dT%H:%M:%S.%f")
        assert new_return_date.date() == updated_found_borrowed.return_date.date() 
        # find copy and print 
        query = select(all_models.Copy).where(all_models.Copy.id == updated_found_borrowed.copy_id)
        found_copy = db.scalar(query)
        assert found_copy.status == "available"
        
        # borrowed with id not found
        response = client.put(
            f"/borrowed/return_borrowed_user/{borrowed_id+1}",
            json=data,
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND
 
 
 # Test case for create borrowed (PUT /borrowed/return_borrowed_any_user/{borrowed_id})
def test_return_borrowed_any_user_with_id(test_db: sessionmaker) -> None:
    """
    This function will be used to test return borrowed with id.
    Parameters:
        test_db: The database session.
    Returns:
        None
    """
    with test_db() as db:
        borrowed_id, copy_id, issue_date, due_date, _ = create_borrowed_entry_in_db(
            test_db, is_librarian=True
        )
        new_return_date = datetime.now()
        new_return_date = new_return_date.isoformat()
        data = {
            "copy_id": copy_id,
            "issue_date": issue_date,
            "due_date": due_date,
            "return_date": new_return_date,
        }
        token = None
        # update request
        response = client.put(
            f"/borrowed/return_borrowed_any_user/{borrowed_id}",
            json=data,
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        token = get_token_for_user(test_db)
         # update request
        response = client.put(
            f"/borrowed/return_borrowed_any_user/{borrowed_id}",
            json=data,
            headers={"Authorization": f"Bearer {token}"},
        )
        query = select(all_models.Borrowed).where(all_models.Borrowed.id == borrowed_id)
        updated_found_borrowed = db.scalar(query)
        # convert new_return_date to date its an str now
        new_return_date = datetime.strptime(new_return_date, "%Y-%m-%dT%H:%M:%S.%f")
        assert new_return_date.date() == updated_found_borrowed.return_date.date() 
        # find copy and print 
        query = select(all_models.Copy).where(all_models.Copy.id == updated_found_borrowed.copy_id)
        found_copy = db.scalar(query)
        assert found_copy.status == "available"
        
        # borrowed with id not found
        response = client.put(
            f"/borrowed/return_borrowed_any_user/{borrowed_id+1}",
            json=data,
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

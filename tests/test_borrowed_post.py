import logging
from datetime import datetime, timedelta

from fastapi import status
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker

from src.models import all_models
from tests.client import client
from tests.test_language_api import create_user_using_model, get_token_for_user


# Test case for create borrowed (POST /borrowed/)
def test_create_borrowed_with_correct_due_date(test_db: sessionmaker) -> None:
    """
    This function will be used to test create borrowed.
    Parameters:
        test_db: The database session.
    Returns:
        None
    """

    with test_db() as db:
        create_user_using_model(test_db, librarian=True)
        language = all_models.Language(language="English")
        genre = all_models.Genre(genre="Fantasy")
        author = all_models.Author(
            first_name="J.K.",
            last_name="Rowling",
            birth_date=datetime(1980, 1, 1),
            death_date=None,
        )
        book = all_models.Book(
            title="Harry Potter",
            description="The boy who lived",
            language=language,
            date_of_publication=datetime(2000, 1, 1),
            isbn="ABCD-1234",
        )
        book.authors.append(author)
        book.genres.append(genre)
        copy = all_models.Copy(book=book, language=language, status="available")
        user = db.scalar(select(all_models.User).where(all_models.User.email == "Test"))
        db.add_all([language, genre, author, book, copy])
        db.commit()
        db.refresh(copy)
        due_date = datetime.now() + timedelta(days=2)
        due_date = due_date.isoformat()
        data = {
            "copy_id": copy.id,
            "user_id": user.id,
            "issue_date": datetime.now().isoformat(),
            "due_date": due_date,
            "return_date": None,
        }
        token = None
        response = client.post(
            "/borrowed", json=data, headers={"Authorization": f"Bearer {token}"}
        )
        logging.info(
            " Response status code with Token = None " + str(response.status_code)
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
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
        assert response.status_code == status.HTTP_201_CREATED
        borrowed = response.json()
        assert borrowed["copy_id"] == copy.id
        assert borrowed["user_id"] == user.id
        assert borrowed["issue_date"][:10] == datetime.now().isoformat()[:10]
        assert borrowed["due_date"] == due_date
        assert borrowed["return_date"] == None
        borrowed_from_db = db.scalar(
            select(all_models.Borrowed).where(
                all_models.Borrowed.copy_id == copy.id
                and all_models.Borrowed.user_id == user.id
            )
        )
        assert borrowed_from_db.copy_id == copy.id
        assert borrowed_from_db.user_id == user.id
        assert (
            borrowed_from_db.issue_date.isoformat()[:10]
            == datetime.now().isoformat()[:10]
        )
        assert borrowed_from_db.due_date == datetime.fromisoformat(due_date)
        assert borrowed_from_db.return_date == None
        logging.info(" Borrowed created successfully and tested successfully")


# Test case for create borrowed (POST /borrowed/)
def test_create_borrowed_with_wrong_due_date(test_db: sessionmaker) -> None:
    """
    This function will be used to test create borrowed.
    Parameters:
        test_db: The database session.
    Returns:
        None
    """
    with test_db() as db:
        create_user_using_model(test_db, librarian=True)
        language = all_models.Language(language="English")
        genre = all_models.Genre(genre="Fantasy")
        author = all_models.Author(
            first_name="J.K.",
            last_name="Rowling",
            birth_date=datetime(1980, 1, 1),
            death_date=None,
        )
        book = all_models.Book(
            title="Harry Potter",
            description="The boy who lived",
            language=language,
            date_of_publication=datetime(2000, 1, 1),
            isbn="ABCD-1234",
        )
        book.authors.append(author)
        book.genres.append(genre)
        copy = all_models.Copy(book=book, language=language, status="available")
        user = db.scalar(select(all_models.User).where(all_models.User.email == "Test"))
        db.add_all([language, genre, author, book, copy])
        db.commit()
        db.refresh(copy)
        due_date = datetime.now() - timedelta(days=2)
        due_date = due_date.isoformat()
        data = {
            "copy_id": copy.id,
            "user_id": user.id,
            "issue_date": datetime.now().isoformat(),
            "due_date": due_date,
            "return_date": None,
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
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        logging.info(" Wrong Due date Tested successfully")


# Test case for create borrowed (POST /borrowed/)
def test_create_borrowed_with_correct_return_date(test_db: sessionmaker) -> None:
    """
    This function will be used to test create borrowed.
    Parameters:
        test_db: The database session.
    Returns:
    """
    with test_db() as db:
        create_user_using_model(test_db, librarian=True)
        language = all_models.Language(language="English")
        genre = all_models.Genre(genre="Fantasy")
        author = all_models.Author(
            first_name="J.K.",
            last_name="Rowling",
            birth_date=datetime(1980, 1, 1),
            death_date=None,
        )
        book = all_models.Book(
            title="Harry Potter",
            description="The boy who lived",
            language=language,
            date_of_publication=datetime(2000, 1, 1),
            isbn="ABCD-1234",
        )
        book.authors.append(author)
        book.genres.append(genre)
        copy = all_models.Copy(book=book, language=language, status="available")
        user = db.scalar(select(all_models.User).where(all_models.User.email == "Test"))
        db.add_all([language, genre, author, book, copy])
        db.commit()
        db.refresh(copy)
        due_date = datetime.now() + timedelta(days=2)
        due_date = due_date.isoformat()
        return_date = datetime.now() - timedelta(days=1)
        return_date = return_date.isoformat()
        data = {
            "copy_id": copy.id,
            "user_id": user.id,
            "issue_date": datetime.now().isoformat(),
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
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        logging.info(" Wrong Return date Tested successfully")

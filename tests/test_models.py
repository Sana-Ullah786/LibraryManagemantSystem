from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import sessionmaker

from src.models import all_models


def test_book_language_relationship(test_db: sessionmaker) -> None:
    """
    A function that tests the book-language relationship and verifies that it is bi-directional
    """
    with test_db() as db:
        # setup
        language = all_models.Language(language="English")
        book = all_models.Book(
            title="Let us C",
            description="Coding book",
            isbn="ABCD1234",
            date_of_publication=datetime(2008, 1, 1),
            language=language,
        )
        db.add_all([book, language])
        db.flush()

        # testing
        book = db.scalar(
            select(all_models.Book).where(all_models.Book.isbn == "ABCD1234")
        )
        language = db.scalar(
            select(all_models.Language).where(all_models.Language.language == "English")
        )
        assert book.language == language
        assert book in language.books


def test_book_author_relationship(test_db: sessionmaker) -> None:
    """
    A function that tests the book-author relationship and verifies that it is bi-directional
    """
    with test_db() as db:
        # setup
        author = all_models.Author(
            first_name="Charles",
            last_name="Babbage",
            birth_date=datetime(1990, 1, 1),
            death_date=datetime(2020, 1, 1),
        )
        language = all_models.Language(language="English")
        book = all_models.Book(
            title="Let us C",
            description="Coding book",
            isbn="ABCD1234",
            date_of_publication=datetime(2008, 1, 1),
            language=language,
        )
        book.authors.append(author)
        db.add_all([book, author, language])
        db.flush()

        # testing
        author = db.scalar(
            select(all_models.Author).where(all_models.Author.first_name == "Charles")
        )
        book = db.scalar(
            select(all_models.Book).where(all_models.Book.isbn == "ABCD1234")
        )
        assert author in book.authors
        assert book in author.books


def test_book_genre_relationship(test_db: sessionmaker) -> None:
    """
    A function that tests the book-genre relationship and verifies that it is bi-directional
    """
    with test_db() as db:
        # setup
        genre = all_models.Genre(genre="Science-Fiction")
        language = all_models.Language(language="English")
        book = all_models.Book(
            title="Let us C",
            description="Coding book",
            isbn="ABCD1234",
            date_of_publication=datetime(2008, 1, 1),
            language=language,
        )
        book.genres.append(genre)
        db.add_all([book, genre, language])
        db.flush()

        # testing
        genre = db.scalar(
            select(all_models.Genre).where(all_models.Genre.genre == "Science-Fiction")
        )
        book = db.scalar(
            select(all_models.Book).where(all_models.Book.isbn == "ABCD1234")
        )
        assert genre in book.genres
        assert book in genre.books


def test_book_copy_relationship(test_db: sessionmaker) -> None:
    """
    A function that tests the book-copy relationship and verifies that it is bi-directional
    """
    with test_db() as db:
        # setup
        status = all_models.Status(status="available")
        language = all_models.Language(language="English")
        book = all_models.Book(
            title="Let us C",
            description="Coding book",
            isbn="ABCD1234",
            date_of_publication=datetime(2008, 1, 1),
            language=language,
        )
        copy = all_models.Copy(book=book, language=language, status=status)
        db.add_all([status, language, book, copy])
        db.flush()

        # testing
        book = db.scalar(
            select(all_models.Book).where(all_models.Book.isbn == "ABCD1234")
        )
        copy = db.scalar(select(all_models.Copy).where(all_models.Copy.book == book))
        assert copy in book.copies
        assert book == copy.book


def test_borrowed(test_db: sessionmaker) -> None:
    """
    A function that tests the borrowed model and it's relationships
    """
    with test_db() as db:
        # setup
        status = all_models.Status(status="available")
        language = all_models.Language(language="English")
        book = all_models.Book(
            title="Let us C",
            description="Coding book",
            isbn="ABCD1234",
            date_of_publication=datetime(2008, 1, 1),
            language=language,
        )
        copy = all_models.Copy(book=book, language=language, status=status)
        user = all_models.User(
            first_name="Mustansir",
            last_name="Muzaffar",
            email="mustansirmuzaffar@folio3.com",
            username="mustansir14",
            password="12345678",
            date_of_joining=datetime.now(),
            contact_number="+92333222444",
            address="Karachi",
            is_active=True,
            is_librarian=False,
        )
        borrowed = all_models.Borrowed(
            user=user,
            copy=copy,
            issue_date=datetime.now(),
            due_date=datetime(2023, 12, 12),
        )
        db.add_all([status, language, book, copy, user, borrowed])
        db.flush()

        # testing
        user = db.scalar(
            select(all_models.User).where(all_models.User.first_name == "Mustansir")
        )
        book = db.scalar(
            select(all_models.Book).where(all_models.Book.isbn == "ABCD1234")
        )
        copy = db.scalar(select(all_models.Copy).where(all_models.Copy.book == book))
        borrowed = db.scalar(
            select(all_models.Borrowed).where(all_models.Borrowed.copy == copy)
        )
        assert borrowed.user == user
        assert borrowed.copy == copy

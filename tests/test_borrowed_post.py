from datetime import datetime, timedelta
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker
from src.models import all_models
from test_auth import register_user, TEST_USER


# Helper function

def create_borrowed(test_db: sessionmaker) -> all_models.Borrowed:

    with test_db() as db:

        register_user(TEST_USER)

        language = all_models.Language(language="English")
        genre = all_models.Genre(genre="Fantasy")
        author = all_models.Author(first_name="J.K.", last_name="Rowling", birth_date=datetime(1980, 1, 1), death_date=None)
        book = all_models.Book(title="Harry Potter", description="The boy who lived", language=language, date_of_publication=datetime(2000, 1, 1), isbn="ABCD-1234")
        book.authors.append(author)
        book.genres.append(genre)
        copy = all_models.Copy(book=book, language=language, status="available")
        user = db.scalar(select(all_models.User).where(all_models.User.email == TEST_USER['email']))
        borrowed = all_models.Borrowed(copy=copy, user=user, issue_date=datetime.now(), due_date=datetime.now() + timedelta(days=2), return_date=None)
        
        db.add_all([language, genre, author, book, copy, borrowed])
        return borrowed
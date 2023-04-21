from authors import Author  # noqa
from book import Books  # noqa
from book_author import BookAuthor  # noqa
from book_genre import Book_Genre  # noqa
from borrowed import Borrowed  # noqa
from copies import Copy  # noqa
from database import Base, engine
from genre import Genre  # noqa
from language import Language  # noqa
from user import Users  # noqa

Base.metadata.create_all(bind=engine)

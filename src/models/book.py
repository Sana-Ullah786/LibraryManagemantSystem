from datetime import datetime

from database import Base, engine
from sqlalchemy import DateTime, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column


class Books(Base):
    """
    A class representing a book in the database.

    Attributes:
        id (int): The primary key ID of the book.
        title (str): The title of the book.
        date_of_publication (datetime): The date of publication of the book.
        isbn (str): The ISBN number of the book.
        description (str): A description of the book.
        language_id (int): The ID of the language the book is written in.
        created_at (datetime): The date and time the book was created.
        updated_at (datetime): The date and time the book was last updated.
    """

    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(32), unique=True, nullable=False)
    date_of_publication: Mapped[datetime] = mapped_column(
        DateTime(), nullable=False
    )  # noqa
    isbn: Mapped[str] = mapped_column(Integer)
    description: Mapped[str] = mapped_column(String(200), nullable=False)
    language_id: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), onupdate=func.now(), nullable=True
    )


# create a table in database
Base.metadata.create_all(bind=engine)


# with Session(engine) as session:
#     book= session.query(Books).filter(Books.title=='Second Book').first()
#     book.isbn = 121
#     session.add(book)
#     session.commit()

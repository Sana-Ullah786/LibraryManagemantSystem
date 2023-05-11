from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.database import Base


class Book(Base):
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

    __tablename__ = "book"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(), nullable=False)
    date_of_publication: Mapped[datetime] = mapped_column(
        DateTime(), nullable=False
    )  # noqa
    isbn: Mapped[str] = mapped_column(String(), unique=True)
    description: Mapped[str] = mapped_column(String(200), nullable=False)
    language_id: Mapped[int] = mapped_column(ForeignKey("language.id"))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), onupdate=func.now(), nullable=True
    )

    authors = relationship(
        "Author", secondary="book_author", back_populates="books", lazy=False
    )
    genres = relationship(
        "Genre", secondary="book_genre", back_populates="books", lazy=False
    )
    copies = relationship("Copy", back_populates="book")
    language = relationship("Language", back_populates="books", lazy=False)

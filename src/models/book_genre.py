from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column

from .database import Base


class BookGenre(Base):
    """
    A class representing the relationship between
    a book and a genre in the database.

    Attributes:
        book_id (int): The ID of the book in the relationship.
        genre_id (int): The ID of the genre in the relationship.
        created_at (datetime): The date and time the relationship was created.
        updated_at (datetime): The date and time the reference was last updated.
    """

    __tablename__ = "book_genre"

    book_id: Mapped[int] = mapped_column(ForeignKey("book.id"), primary_key=True)
    genre_id: Mapped[int] = mapped_column(ForeignKey("genre.id"), primary_key=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), onupdate=func.now(), nullable=True
    )

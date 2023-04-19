from datetime import datetime

from database import Base, engine
from sqlalchemy import DateTime, Integer, func
from sqlalchemy.orm import Mapped, mapped_column


class Book_Genre(Base):
    """
    A class representing the relationship between
    a book and a genre in the database.

    Attributes:
        id (int): The primary key ID of the relationship.
        book_id (int): The ID of the book in the relationship.
        genre_id (int): The ID of the genre in the relationship.
        created_at (datetime): The date and time the relationship was created.
    """

    __tablename__ = "book_genre"

    id: Mapped[int] = mapped_column(primary_key=True)
    book_id: Mapped[int] = mapped_column(Integer)
    genre_id: Mapped[int] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )


# create table in database
Base.metadata.create_all(bind=engine)

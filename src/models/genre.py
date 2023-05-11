from datetime import datetime

from sqlalchemy import DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


class Genre(Base):

    """
    A class representing a genre in the database.

    Attributes:
        id (int): The primary key ID of the genre.
        genre (str): The name of the genre.
        created_at (datetime): The date and time the genre was created.
        updated_at (datetime): The date and time the genre was last updated.
    """

    __tablename__ = "genre"

    id: Mapped[int] = mapped_column(primary_key=True)
    genre: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()  # noqa
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), onupdate=func.now(), nullable=True
    )

    books = relationship("Book", secondary="book_genre", back_populates="genres")

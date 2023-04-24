from datetime import datetime

from sqlalchemy import DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


class Author(Base):
    """
    A class representing a Authors of all the available books in libraray.
    Attributes:
        id (int): The primary key ID of the book.
        first_name (str): First name of the author.
        last_name (str): Last name of the author.
        birth_date (date): Birth date of the author.
        death_date (date): Death date of the author.
        created_at (datetime): The date and time the author was created.
        updated_at (datetime): The date and time the author was last updated.
    """

    __tablename__ = "author"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(32), nullable=False)
    last_name: Mapped[str] = mapped_column(String(32), nullable=False)
    birth_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    death_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), onupdate=func.now(), nullable=True
    )

    books = relationship("Book", secondary="book_author", back_populates="authors")

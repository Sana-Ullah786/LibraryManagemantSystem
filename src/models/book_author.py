from datetime import datetime

from database import Base
from sqlalchemy import DateTime, Integer, func
from sqlalchemy.orm import Mapped, mapped_column


class BookAuthor(Base):
    """
    A class representing an associate table between book and its author.
    Attributes:
        id (int): The primary key ID of the book.
        author_id (int): Reference to the author table.
        book_id (int): Reference to the Book table.
        created_at (datetime): The date and time the reference was created.
        updated_at (datetime): The date and time the reference \n
            was last updated.
    """

    __tablename__ = "BookAuthor"

    id: Mapped[int] = mapped_column(primary_key=True)
    author_id: Mapped[int] = mapped_column(Integer())
    book_id: Mapped[int] = mapped_column(Integer())
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), onupdate=func.now()
    )

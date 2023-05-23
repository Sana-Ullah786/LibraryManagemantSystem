from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column

from src.models.database import Base


class BookAuthor(Base):
    """
    A class representing an associate table between book and its author.
    Attributes:
        author_id (int): Reference to the author table.
        book_id (int): Reference to the Book table.
        created_at (datetime): The date and time the reference was created.
        updated_at (datetime): The date and time the reference \n
            was last updated.
    """

    __tablename__ = "book_author"

    author_id: Mapped[int] = mapped_column(ForeignKey("author.id"), primary_key=True)
    book_id: Mapped[int] = mapped_column(ForeignKey("book.id"), primary_key=True)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), onupdate=func.now(), nullable=True
    )

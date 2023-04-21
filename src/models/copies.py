from datetime import datetime

from book import Books
from database import Base
from sqlalchemy import DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column


class Copy(Base):
    """
    A class representing a copies of all the available books in libraray.
    Attributes:
        id (int): The primary key ID of the book.
        book_id (int): Reference to book whose copy is it.
        language_id (int): The language of that certain copy.
        status (str): Borrowed status of the copy \n
            (Available, Loaned out, Reserved, Maintenance)
        created_at (datetime): The date and time the copy was created.
        updated_at (datetime): The date and time the copy was last updated.
    """

    __tablename__ = "Copies"

    id: Mapped[int] = mapped_column(primary_key=True)
    book_id: Mapped[int] = mapped_column(
        Integer(), ForeignKey(Books.id), nullable=False
    )
    language_id: Mapped[int] = mapped_column(
        Integer(), ForeignKey("Languages.id"), nullable=False
    )
    status: Mapped[str] = mapped_column(String(32), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), onupdate=func.now()
    )

    # This table has 2 relations (with Books and Languages) that must be made.

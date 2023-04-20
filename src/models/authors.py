from datetime import datetime

from database import Base
from sqlalchemy import DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column


class Author(Base):
    """
    A class representing a Authors of all the available books in libraray.
    Attributes:
        id (int): The primary key ID of the book.
        f_name (str): First name of the author.
        l_name (str): Last name of the author.
        created_at (datetime): The date and time the author was created.
        updated_at (datetime): The date and time the author was last updated.
    """

    __tablename__ = "Authors"

    id: Mapped[int] = mapped_column(primary_key=True)
    f_name: Mapped[str] = mapped_column(String(32), nullable=False)
    l_name: Mapped[str] = mapped_column(String(32), nullable=False)
    birth_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    death_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), onupdate=func.now()
    )

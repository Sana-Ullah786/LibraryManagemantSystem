from datetime import datetime

from database import Base
from sqlalchemy import DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column


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
    genre: Mapped[str] = mapped_column(String(32), unique=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), onupdate=func.now(), nullable=True
    )

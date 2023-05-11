from datetime import datetime

from sqlalchemy import DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.database import Base


class Language(Base):
    """
    A class representing a Languages available in the database.

    Attributes:
        id (int): The primary key ID.
        language (str): The string representing language.
        created_at (datetime): The date and time the language was created.
        updated_at (datetime): The date and time the language was last updated.
    """

    __tablename__ = "language"

    id: Mapped[int] = mapped_column(primary_key=True)
    language: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), onupdate=func.now(), nullable=True
    )

    books = relationship("Book", back_populates="language")
    copies = relationship("Copy", back_populates="language")

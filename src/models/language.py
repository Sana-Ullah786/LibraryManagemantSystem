from datetime import datetime

from database import Base
from sqlalchemy import DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column


class Language(Base):
    """
    A class representing a Languages available in the database.

    Attributes:
        id (int): The primary key ID.
        language (str): The string representing language.
        created_at (datetime): The date and time the language was created.
        updated_at (datetime): The date and time the language was last updated.
    """

    __tablename__ = "Languages"

    id: Mapped[int] = mapped_column(primary_key=True)
    language: Mapped[str] = mapped_column(String(32), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), onupdate=func.now(), nullable=True
    )

from datetime import datetime

from sqlalchemy import DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column

from .database import Base


class Status(Base):
    """
    A class representing a Status available in the database.

    Attributes:
        id (int): The primary key ID.
        status (str): The string representing status.
        created_at (datetime): The date and time the Status was created.
        updated_at (datetime): The date and time the status was last updated.
    """

    __tablename__ = "status"

    id: Mapped[int] = mapped_column(primary_key=True)
    status: Mapped[str] = mapped_column(String(32), nullable=False, unique=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), onupdate=func.now(), nullable=True
    )

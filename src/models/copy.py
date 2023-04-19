from datetime import datetime

from database import Base
from sqlalchemy import DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column


class Copy(Base):
    """
    Database model to store copies of a specific book available and there \n
    status.
    """

    __tablename__ = "Copies"

    id: Mapped[int] = mapped_column(primary_key=True)
    book_id: Mapped[int] = mapped_column(
        Integer(), ForeignKey("Books.id"), nullable=False
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

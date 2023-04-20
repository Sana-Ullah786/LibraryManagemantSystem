from datetime import datetime

from database import Base
from sqlalchemy import DateTime, ForeignKey, Integer, func, mapped_column
from sqlalchemy.orm import Mapped, relationship


class Borrowed(Base):
    """
    This is the borrowed model that will be used to create the borrowed table.
    Also, this will be used to create the borrowed object.
    """

    __tablename__ = "borrowed"
    id: Mapped[int] = mapped_column(Integer(), primary_key=True, index=True)
    copy_id: Mapped[int] = mapped_column(Integer(), ForeignKey("copies.id"))
    user_id: Mapped[int] = mapped_column(Integer(), ForeignKey("users.id"))
    issue_date: Mapped[datetime] = mapped_column(DateTime)
    due_date: Mapped[datetime] = mapped_column(DateTime)
    return_date: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), onupdate=func.now(), nullable=True
    )
    # Relationship with the user model
    user = relationship("Users", back_populates="borrowed")
    # TODO: Relationship with copies

from datetime import datetime
from sqlalchemy import Boolean, mapped_column, Integer, String, DateTime, func
from database import Base
from sqlalchemy.orm import Mapped, mapped_column


class Users(Base):
    """
    This is the user model that will be used to create the users table in the database.
    And will be used to create the user object.
    """
    __tablename__ = "users"
    id: int = mapped_column(Integer(), primary_key=True, index=True)
    email: str = mapped_column(String(32), unique=True, index=True)
    username: str = mapped_column(String(32), unique=True, index=True)
    first_name: str = mapped_column(String(32))
    last_name: str = mapped_column(String(32))
    date_of_joining: datetime = mapped_column(DateTime)
    contact_number: str = mapped_column(String(32))
    address: str = mapped_column(String(200))
    is_librarian: bool = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), onupdate=func.now(),nullable=True)
    
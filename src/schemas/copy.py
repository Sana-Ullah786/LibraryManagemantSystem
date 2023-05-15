from typing import Optional

from pydantic import BaseModel, Field, validator


class CopySchema(BaseModel):
    book_id: Optional[int] = Field(None, gt=-1)
    language_id: Optional[int] = Field(
        None, title="Enter Language Id for book language"
    )
    status: str = Field(..., title="Specify book status")

    class Config:
        schema_extra = {
            "example": {
                "book_id": 1,
                "language_id": 1,
                "status": "Available",
            }
        }

    @validator("book_id")
    def validate_book_id(cls, value):
        if value is not None and value <= 0:
            raise ValueError("Invalid book ID")
        return value

    @validator("language_id")
    def validate_language_id(cls, value):
        if value is not None and value <= 0:
            raise ValueError("Invalid language ID")
        return value

    @validator("status")
    def validate_status(cls, value):
        statuses = ["available", "reserved", "maintenance", "loaned"]
        if not value.strip():
            raise ValueError("Status cannot be empty or contain only whitespace")
        if value not in statuses:
            raise ValueError("Status not found")
        return value.strip()

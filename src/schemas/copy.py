from typing import Optional

from pydantic import BaseModel, Field, validator


class CopySchema(BaseModel):
    book_id: Optional[int] = None
    language_id: Optional[int] = Field(
        None, title="Enter Language Id for book language"
    )
    status_id: int = Field(..., title="Specify book status")

    class Config:
        schema_extra = {
            "example": {
                "book_id": 1,
                "language_id": 1,
                "status_id": 1,
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

    @validator("status_id")
    def validate_status_id(cls, value):
        if value is not None and value <= 0:
            raise ValueError("Invalid status ID")
        return value

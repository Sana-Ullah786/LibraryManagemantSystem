from datetime import date
from typing import List, Optional

from pydantic import BaseModel, Field, validator


class BookSchema(BaseModel):
    id: Optional[int] = None
    title: str = Field(..., min_length=1, description="Title of the book")
    date_of_publication: str = Field(
        ..., description="Date of publication in ISO format (YYYY-MM-DD)"
    )
    isbn: str = Field(..., min_length=10, max_length=13, description="ISBN of the book")
    description: str = Field(
        "",
        max_length=200,
        description="Short description of the book (max 200 characters)",
    )
    language_id: int = Field(..., gt=0, description="Language ID of the book")
    author_ids: List[int] = Field(..., min_items=1, description="List of author IDs")
    genre_ids: List[int] = Field(..., min_items=1, description="List of genre IDs")
    no_of_copies: int = Field(default=1)

    @validator("date_of_publication")
    def validate_date_of_publication(cls, value):
        if not value:
            raise ValueError("Date of publication cannot be empty")
        input_date = date.fromisoformat(value)
        if input_date > date.today():
            raise ValueError("Date of publication cannot be in the future")
        return value

    @validator("title")
    def validate_title(cls, value):
        if not value.strip():
            raise ValueError("Title cannot be empty or contain only whitespace")
        return value.strip()

    @validator("language_id")
    def validate_language_id(cls, value):
        if not isinstance(value, int):
            raise ValueError("Language ID must be an integer")
        if value <= 0:
            raise ValueError("Invalid Language ID")
        return value

    class Config:
        schema_extra = {
            "example": {
                "title": "Title of the book",
                "isbn": "dsa135",
                "date_of_publication": "2022-03-02",
                "description": "Short dics about book, max 200 characters",
                "language_id": 3,
                "author_ids": [1, 2],
                "genre_ids": [1, 2],
            }
        }

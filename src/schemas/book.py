from datetime import date, datetime
from typing import List, Optional

from pydantic import BaseModel, Field, validator


class BookSchema(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length=1)
    date_of_publication: str = Field()
    isbn: str = Field(min_length=10, max_length=13)
    description: str = Field(min_length=0, max_length=200)
    language_id: int = Field()
    author_ids: List[int] = Field(min_items=1)
    genre_ids: List[int] = Field(min_items=1)

    @validator("date_of_publication")
    def validate_my_date(cls, value):
        if len(value) < 0:
            raise ValueError("Can`t be an empty Field")
        input_date = date.fromisoformat(value)
        if input_date > date.today():
            raise ValueError("Date can't be greater than today")
        return value

    @validator("title")
    def validate_title(cls, value):
        if len(value) < 1:
            raise ValueError("Title Field can`t be empty")
        return value

    @validator("language_id")
    def validate_language(cls, value):
        if value is None:
            raise ValueError("Language cant`t be empty or a string")
        if value == 0:
            raise ValueError("Invalid Language ID ")
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

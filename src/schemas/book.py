from datetime import date, datetime
from typing import List, Optional

from pydantic import BaseModel, Field, validator


class BookSchema(BaseModel):
    id: Optional[int] = None
    title: str = Field()
    date_of_publication: str = Field()
    isbn: str = Field()
    description: str = Field(min_length=0, max_length=200)
    language_id: int = Field()
    author_ids: List[int] = Field()
    genre_ids: List[int] = Field()

    @validator("date_of_publication")
    def validate_my_date(cls, value):
        input_date = date.fromisoformat(value)
        if input_date > date.today():
            raise ValueError("Date can't be greater than today")
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

from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, Field, validator


class BookSchema(BaseModel):
    id: Optional[int] = None
    title: str = Field()
    date_of_publication: datetime = Field()
    isbn: str = Field()
    description: str = Field(min_length=0, max_length=200)
    language_id: int = Field()

    @validator("date_of_publication")
    def pub_date_greater_than_current(cls, v):
        if v > date.today():
            raise ValueError("publication date can't be greater than today.")

    class Config:
        schema_extra = {
            "example": {
                "id": "intger that uniquely identify book.",
                "title": "Title of the book",
                "isbn": "A unique isbn number",
                "description": "Short dics about book, max 200 characters",
                "language_id": "Id of the languages available in db",
            }
        }

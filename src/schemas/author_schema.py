from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, constr, validator


class AuthorSchema(BaseModel):

    """
    Pydantic models for Author model

    """

    id: Optional[int] = None
    first_name: constr(strip_whitespace=True, min_length=1, max_length=32)
    last_name: constr(strip_whitespace=True, min_length=1, max_length=32)
    birth_date: datetime = Field(title="Date of Birth For The Author")
    death_date: datetime = Field(title="Date of Passing For The Author", default=None)

    @validator("death_date")
    def birth_date_greater_than_death_date(cls, v, values, **kwargs):
        if "birth_date" in values and v.date() < values["birth_date"].date():
            raise ValueError("Death Date must be greater than Birth Date")
        return v

    class Config:
        schema_extra = {
            "example": {
                "first_name": "John",
                "last_name": "Doe",
                "birth_date": datetime(2023, 4, 26),
                "death_date": datetime(2023, 4, 26),
            }
        }

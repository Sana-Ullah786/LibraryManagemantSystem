from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, validator


class AuthorSchema(BaseModel):

    """
    Pydantic models for Author model

    """

    user_id: Optional[int] = None
    first_name: str = Field(title="First name of Author ")
    last_name: str = Field(title="Last name of Author ")
    birth_date: datetime = Field(title="Date of Birth For The Author")
    death_date: datetime = Field(title="Date of Passing For The Author", default=None)

    @validator("death_date")
    def birth_date_greater_than_death_date(cls, v, values, **kwargs):
        if "birth_date" in values and values["death_date"] >= values["birth_date"]:
            raise ValueError("Death Date must be greater than Birth Date")

    class Config:
        schema_extra = {
            "example": {
                "first_name": "John",
                "last_name": "Doe",
                "birth_date": "11/8/1981",
                "death_date": "21/12/2022",
            }
        }

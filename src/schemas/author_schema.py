from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

"""
Pydantic models for Author model

"""


class UserModel(BaseModel):
    user_id: Optional[int] = None
    first_name: str = Field(title="First name of Author ")
    last_name: str = Field(title="Last name of Author ")
    birth_date: datetime = Field(title="Date of Birth For The Author")
    death_date: datetime = Field(title="Date of Passing For The Author", default=None)


class Config:
    schema_extra = {
        "example": {
            "first_name": "John",
            "last_name": "Doe",
            "birth_date": "11/8/1981",
            "death_date": "21/12/2022",
        }
    }

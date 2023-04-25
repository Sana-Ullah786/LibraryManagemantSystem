from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, Field, validator


class UserSchema(BaseModel):
    """
    Pydantic model that will we used to send data to and from routes.
    Has attributes and validations as of DB.
    """

    id: Optional[int] = None
    email: str = Field(min_length=0, max_length=32)
    username: str = Field(min_length=0, max_length=32)
    password: str = Field(min_length=0, max_length=8)
    first_name: str = Field(min_length=0, max_length=32)
    last_name: str = Field(min_length=0, max_length=32)
    date_of_joining: datetime = Field()
    contact_number: str = Field(min_length=0, max_length=32)
    address: str = Field(min_length=0, max_length=200)

    @validator("date_of_joining")
    def join_date_greater_than_current(cls, v):
        if v > date.today():
            raise ValueError("joining date can't be greater than today.")

    class Config:
        schema_extra = {
            "example": {
                "email": "A unique email",
                "username": "A unique username",
                "password": "8 character string that can be used to login",
                "first_name": "Users first name",
                "last_name": "Users last name",
                "contact_number": "users cellphone number",
                "address": "users physical address",
            }
        }

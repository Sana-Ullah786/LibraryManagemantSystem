import re
from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, constr, validator

from src.models.user import User


class UserSchemaBase(BaseModel):
    """
    A Base Pydantic model for user.
    """

    email: EmailStr
    username: constr(strip_whitespace=True, min_length=3, max_length=32)
    first_name: constr(strip_whitespace=True, min_length=1, max_length=32)
    last_name: constr(strip_whitespace=True, min_length=1, max_length=32)
    contact_number: constr()
    address: constr(strip_whitespace=True, min_length=3, max_length=200)


class UserSchemaIn(UserSchemaBase):

    """
    A Pydantic user schema which will be used to create a new user.
    """

    password: constr(min_length=8, max_length=100)

    @validator("password")
    def check_password(cls, v):
        pattern = r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&_*-]).{8,}$"
        if not re.match(pattern, v):
            raise ValueError(
                "Password must contain at least one lowercase letter, one uppercase letter, one digit, one special character and must be at least 8 characters long."
            )
        return v

    @validator("contact_number")
    def check_contact_number(cls, v):
        pattern = r"^\d{11}$"
        if not re.match(pattern, v):
            raise ValueError("Contact number should have 11 digits.")
        return v

    class Config:
        schema_extra = {
            "example": {
                "email": "johndoe@gmail.com",
                "username": "johndoe123",
                "password": "John_Doe987",
                "first_name": "John",
                "last_name": "Doe",
                "contact_number": "03411231231",
                "address": "Folio3 Tower, Shahrah-e-Faisal, Karachi, Pakistan",
            }
        }


class UserSchemaOut(UserSchemaBase):

    """
    A Pydantic user schema which will be used to return the user.
    """

    id: int
    date_of_joining: datetime
    is_librarian: bool


class UserSchemaToken(UserSchemaOut):

    """
    A Pydantic user schema that will be used to return the token as well as other user information when a user logs in
    """

    token: str

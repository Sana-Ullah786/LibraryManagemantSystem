import re
from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, constr, validator


class UserSchema(BaseModel):
    """
    Pydantic model that will we used to send data to and from routes.
    Has attributes and validations as of DB.
    """

    id: Optional[int] = None
    email: EmailStr
    username: constr(strip_whitespace=True, min_length=3, max_length=32)
    password: constr(min_length=8, max_length=100)
    first_name: constr(strip_whitespace=True, min_length=1, max_length=32)
    last_name: constr(strip_whitespace=True, min_length=1, max_length=32)
    date_of_joining: Optional[datetime]
    contact_number: constr()
    address: constr(strip_whitespace=True, min_length=3, max_length=200)

    @validator("date_of_joining")
    def join_date_greater_than_current(cls, v):
        if v.date() > date.today():
            raise ValueError("joining date can't be greater than today.")
        return v

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

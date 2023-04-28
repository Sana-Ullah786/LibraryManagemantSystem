from datetime import date, datetime
from typing import Optional

from pydantic import Field, validator

from .user import UserSchema


class UpdateUserSchema(UserSchema):
    """
    Pydantic model that will we used to update user model
    """

    old_password: str = Field(min_length=0, max_length=8)

    class Config:
        schema_extra = {
            "example": {
                "email": "A unique email",
                "username": "A unique username",
                "password": "8 character string that can be used to login",
                "old_password": "Must match with current password",
                "first_name": "Users first name",
                "last_name": "Users last name",
                "contact_number": "users cellphone number",
                "address": "users physical address",
            }
        }

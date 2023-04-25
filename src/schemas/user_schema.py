from pydantic import BaseModel, Field


class UserSchema(BaseModel):
    """
    Pydantic model that will we used to send data to and from routes.
    Has attributes and validations as of DB.
    """

    email: str = Field(
        min_length=0, max_length=32
    )  # mapped_column(String(32), unique=True, index=True)
    username: str = Field(
        min_length=0, max_length=32
    )  # mapped_column(String(32), unique=True, index=True)
    password: str = Field(
        min_length=0, max_length=8
    )  # mapped_column(String, unique=True, index=True)
    first_name: str = Field(
        min_length=0, max_length=32
    )  # mapped_column(String(32)) #noqa
    last_name: str = Field(
        min_length=0, max_length=32
    )  # mapped_column(String(32)) #noqa
    # date_of_joining: datetime = mapped_column(DateTime)
    contact_number: str = Field(
        min_length=0, max_length=32
    )  # mapped_column(String(32))
    address: str = Field(
        min_length=0, max_length=200
    )  # mapped_column(String(200)) #noqa

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

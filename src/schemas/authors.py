from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class UserModel(BaseModel):
    user_id: Optional[int] = None
    first_name: str = Field(title="First name of Author ")
    last_name: str = Field(title="Last name of Author ")
    birth_date: datetime = Field(title="Date of Birth For The Author")
    death_date: datetime = Field(title="Date of Passing For The Author", default=None)

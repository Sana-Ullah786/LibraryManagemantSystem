from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, validator


class BorrowedSchema(BaseModel):
    """
    The Pydantic Schema model for the Borrowed model
    """

    id: Optional[int] = None
    copy_id: int = Field(title="The ID of the copy to be borrowed")
    user_id: str = Field(title="The ID of the user who is borrowing")
    issue_date: datetime = Field(title="Date on which book was issued")
    due_date: datetime = Field(title="Date on which book return is due")
    return_date: datetime = Field(title="Date on which book is returned by the user")

    @validator("due_date")
    def due_date_greater_than_issue_date(cls, v, values, **kwargs):
        if "issue_date" in values and values["issue_date"] >= values["due_date"]:
            raise ValueError("Due Date must be greater than Issue Date")

    @validator("return_date")
    def return_date_greater_than_issue_date(cls, v, values, **kwargs):
        if "issue_date" in values and values["issue_date"] >= values["return_date"]:
            raise ValueError("Return Date must be greater than Issue Date")

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "copy_id": 3,
                "user_id": 7,
                "issue_date": datetime(2023, 4, 26),
                "due_date": datetime(2023, 4, 30),
                "return_date": None,
            }
        }

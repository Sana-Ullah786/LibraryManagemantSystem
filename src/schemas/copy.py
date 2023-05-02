from typing import Optional

from pydantic import BaseModel, Field


class CopySchema(BaseModel):

    """
    Pydantic models for Copies model

    """

    book_id: Optional[int] = None
    language_id: Optional[int] = Field(
        None, title="Enter Language Id for book language"
    )
    status: str = Field(title="Specify book status")

    class Config:
        schema_extra = {
            "example": {
                "book_id": 1,
                "language_id": 1,
                "status": " Available",
            }
        }

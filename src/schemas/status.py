from typing import Optional

from pydantic import BaseModel, Field


class StatusSchema(BaseModel):

    """
    Pydantic models for Language model

    """

    status_id: Optional[int] = Field(None, title="Language Id ")
    status: str = Field(
        title="Enter Status ", max_length=32, min_length=1, unique_items=True
    )

    class Config:
        schema_extra = {"example": {"status": "Available"}}

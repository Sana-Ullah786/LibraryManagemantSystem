from typing import Optional

from pydantic import BaseModel, Field


class StatusSchema(BaseModel):

    """
    Pydantic models for Language model

    """

    status_id: Optional[int] = Field(
        None,
    )
    status: str = Field(title="Enter Status ", max_length=32, min_length=1)

    class Config:
        schema_extra = {"example": {"status": "available"}}

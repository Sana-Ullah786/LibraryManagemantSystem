from typing import Optional

from pydantic import BaseModel, Field


class LanguageSchema(BaseModel):

    """
    Pydantic models for Language model

    """

    language_id: Optional[int] = Field(None, title="Language Id", gt=0)
    language: str = Field(title="Enter Language Name", max_length=50, min_length=2)

    class Config:
        schema_extra = {"example": {"language": "Language name"}}

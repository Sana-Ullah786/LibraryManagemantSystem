from typing import Optional

from pydantic import BaseModel, Field, constr


class LanguageSchema(BaseModel):

    """
    Pydantic models for Language model

    """

    language_id: Optional[int] = Field(None, title="Language Id", gt=-1)
    language: constr(max_length=50, min_length=2) = Field(title="Enter Language Name")

    class Config:
        schema_extra = {"example": {"language": "Language name"}}

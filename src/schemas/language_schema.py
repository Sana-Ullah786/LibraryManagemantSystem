from typing import Optional

from pydantic import BaseModel, Field

"""
Pydantic models for Language model

"""


class LanguageModel(BaseModel):
    language_id: Optional[int] = Field(None, title="Language Id ")
    language: str = Field(title="Enter Language Name", max_length=32)


class Config:
    schema_extra = {"example": {"language": "Language name"}}

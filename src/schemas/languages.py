from typing import Optional

from pydantic import BaseModel, Field


class LanguageModel(BaseModel):
    language_id: Optional[int] = Field(None, title="Language Id ")
    language: str = Field(title="Enter Language Name")

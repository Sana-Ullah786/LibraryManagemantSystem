from typing import Optional

from pydantic import BaseModel, Field


class GenreSchema(BaseModel):
    id: Optional[int] = Field(None, title="Genre Id", gt=0)
    genre: str = Field(title="Enter Genre Name", max_length=50, min_length=3)

    class Config:
        schema_extra = {
            "example": {
                "id": "intger that uniquely identify genre.",
                "genre": "Name of the genre.",
            }
        }

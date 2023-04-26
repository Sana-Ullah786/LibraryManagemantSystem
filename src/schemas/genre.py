from typing import Optional

from pydantic import BaseModel, Field


class GenreSchema(BaseModel):
    id: Optional[int] = None
    genre: str = Field()

    class Config:
        schema_extra = {
            "example": {
                "id": "intger that uniquely identify genre.",
                "genre": "Name of the genre.",
            }
        }

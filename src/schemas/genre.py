from typing import Optional

from pydantic import BaseModel, Field, constr


class GenreSchema(BaseModel):
    id: Optional[int] = Field(None, title="Genre Id", gt=-1)
    genre: constr(strip_whitespace=True, min_length=3, max_length=50) = Field(
        title="Enter Genre Name"
    )

    class Config:
        schema_extra = {
            "example": {
                "id": "intger that uniquely identify genre.",
                "genre": "Name of the genre.",
            }
        }

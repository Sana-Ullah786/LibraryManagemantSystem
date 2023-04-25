from pydantic import BaseModel, Field


class GenreSchema(BaseModel):
    genre: str = Field()  # mapped_column(String(), unique=True)

    class Config:
        schema_extra = {
            "example": {
                "genre": "Name of the genre.",
            }
        }

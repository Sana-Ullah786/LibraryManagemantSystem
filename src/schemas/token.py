from pydantic import BaseModel, Field


class TokenSchema(BaseModel):
    refresh_token: str = Field(None, title="JWT Token")

    class Config:
        schema_extra = {
            "example": {
                "refresh_token": "String representing JWT token.",
            }
        }

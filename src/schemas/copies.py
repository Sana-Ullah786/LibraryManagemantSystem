from typing import Optional

from pydantic import BaseModel, Field


class CopiesModel(BaseModel):
    book_id: Optional[int] = None
    language_id: Optional[int] = Field(
        None, title="Enter Language Id for book language"
    )
    status: str = Field(title="Specify book status")

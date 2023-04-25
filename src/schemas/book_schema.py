from pydantic import BaseModel, Field


class BookSchema(BaseModel):
    title: str = Field()  # mapped_column(String(), nullable=False)
    # date_of_publication: datetime = Field()
    isbn: str = Field()  # mapped_column(String(), unique=True)
    description: str = Field(
        min_length=0, max_length=200
    )  # mapped_column(String(200), nullable=False)
    language_id: int = Field()  # mapped_column(ForeignKey("language.id"))

    class Config:
        schema_extra = {
            "example": {
                "title": "Title of the book",
                "isbn": "A unique isbn number",
                "description": "Short dics about book, max 200 characters",
                "language_id": "Id of the languages available in db",
            }
        }

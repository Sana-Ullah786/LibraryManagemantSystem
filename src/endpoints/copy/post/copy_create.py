import logging

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from src.dependencies import get_current_librarian, get_db
from src.endpoints.copy.router_init import router
from src.models.copy import Copy
from src.schemas.copy import CopySchema


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=None)
async def copy_create(
    copy: CopySchema,
    db: Session = Depends(get_db),
    librarian: dict = Depends(get_current_librarian),  # noqa
) -> dict:
    """
    Endpoint to create a copy
    """
    logging.info(f"Copy Create Request by Librarian {librarian['id']}")

    copy_model = Copy()
    copy_model.book_id = copy.book_id
    copy_model.language_id = copy.language_id
    copy_model.status_id = copy.status_id

    db.add(copy_model)
    db.commit()
    logging.info(
        f"Copy with id : {copy_model.id} Created by Librarian {librarian['id']}"
    )
    return succesful_response()


def http_exception() -> dict:
    return HTTPException(status_code=404, detail="Copy not found")


def succesful_response() -> dict:
    return {"status": 201, "transaction": "succesful_response"}

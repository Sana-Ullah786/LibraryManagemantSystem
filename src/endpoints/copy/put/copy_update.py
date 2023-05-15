import logging

from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette import status

from src.dependencies import get_current_librarian, get_db
from src.endpoints.copy.router_init import router
from src.models.copy import Copy
from src.schemas.copy import CopySchema


@router.put("/{copy_id}", status_code=status.HTTP_200_OK, response_model=None)
async def copy_update(
    copy_id: int,
    copy: CopySchema,
    db: Session = Depends(get_db),
    librarian: dict = Depends(get_current_librarian),  # noqa
) -> Copy:
    """
    Endpoint to Update an existing copy by ID.
    \n
    Parameter:
    ----------\n
    copy_id : Id of Copy to update.
    copy: Copy Schema Json.
    db : Session.
    librarian : Librarian Credentials.

    Returns:
    -------- \n
    """
    logging.info(
        f"Book Update with id :{copy_id} Request by Librarian {librarian['id']}"
    )

    copy_model = db.execute(select(Copy).where(Copy.id == copy_id)).scalars().first()

    if copy_model is None:
        logging.info(f"Book Update with id :{copy_id} , not found")
        raise http_exception()

    copy_model.book_id = copy.book_id
    copy_model.language_id = copy.language_id
    copy_model.status = copy.status

    db.add(copy_model)
    db.commit()
    db.refresh(copy_model)
    logging.info(
        f"Book Updated with id :{copy_id} Request by Librarian {librarian['id']}"
    )

    return copy_model


def http_exception() -> dict:
    return HTTPException(status_code=404, detail="Copy not found")


def succesful_response() -> dict:
    return {"status": 201, "transaction": "succesful_response"}

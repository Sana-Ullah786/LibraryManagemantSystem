import logging

from fastapi import Depends, HTTPException
from sqlalchemy import delete, select
from sqlalchemy.orm import Session
from starlette import status

from src.dependencies import get_current_librarian, get_db
from src.endpoints.copy.router_init import router
from src.models.copy import Copy


@router.delete("/{copy_id}", status_code=status.HTTP_200_OK)
async def copy_delete(
    copy_id: int,
    db: Session = Depends(get_db),
    librarian: dict = Depends(get_current_librarian),  # noqa
) -> dict:
    """
    Endpoint to delete a copy by ID.\n
    Parameters:
    ----------- \n
    copy_id: Copy Id.\n
    db : db Session. \n
    librarian : Librarian Credentials \n
    Returns:
    ------- \n
    Succesful Response / Failed Response


    """
    logging.info(
        f"Book Delete with id :{copy_id} Request by Librarian {librarian['id']}"
    )

    copy_model = db.execute(select(Copy).where(Copy.id == copy_id)).scalars().first()

    if copy_model is None:
        raise http_exception()

    db.execute(delete(Copy).where(Copy.id == copy_id))
    db.commit()
    logging.info(
        f"Book Updated with id :{copy_id} Request by Librarian {librarian['id']}"
    )

    return succesful_response()


def http_exception() -> dict:
    return HTTPException(status_code=404, detail="Copy not found")


def succesful_response() -> dict:
    return {"status": 201, "transaction": "succesful_response"}

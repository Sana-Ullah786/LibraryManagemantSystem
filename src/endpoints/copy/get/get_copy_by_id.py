import logging

from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette import status

from src.dependencies import get_db
from src.endpoints.copy.router_init import router
from src.models.copy import Copy


@router.get("/{copy_id}", status_code=status.HTTP_200_OK, response_model=None)
async def get_copy_by_id(copy_id: int, db: Session = Depends(get_db)) -> Copy:
    """
    Endpoint to get copy by id
    \n
    Parameter:
    ----------\n
    copy_id : Copy Id of the copy to get.
    db : Session

    Returns:
    -------- \n
    Copy object
    """
    copy = db.execute(select(Copy).where(Copy.id == copy_id)).scalars().first()
    if copy:
        logging.info(f"Copy with copy id : {copy_id}")
        return copy
    if not copy:
        logging.info(f"No Copy with copy id : {copy_id}")
        raise http_exception()


def http_exception() -> dict:
    return HTTPException(status_code=404, detail="Copy not found")


def succesful_response() -> dict:
    return {"status": 201, "transaction": "succesful_response"}

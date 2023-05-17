import logging

from fastapi import Depends
from sqlalchemy import delete
from sqlalchemy.orm import Session
from starlette import status

from src.dependencies import get_db
from src.endpoints.status.router_init import router
from src.models.status import Status


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT, response_model=None)
async def status_delete(
    status_id: int,
    db: Session = Depends(get_db),
) -> None:
    """ "
    Deletes the Status on status ID.
    Params
    ------
    JWT token of librarian.\n
    status_id: int
    Returns
    ------
    Status code 204 NO_CONTENT
    """
    if db.execute(delete(Status).where(Status.id == status_id)).rowcount > 0:
        logging.info(f"Deleting status {status_id} -- {__name__}")
        db.commit()
    else:
        raise ValueError("Undefined Error")

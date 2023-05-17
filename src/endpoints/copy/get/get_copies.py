import logging
from typing import List

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette import status

from src.dependencies import get_db
from src.endpoints.copy.router_init import router
from src.models.copy import Copy
from src.responses import custom_response


@router.get("/", status_code=status.HTTP_200_OK, response_model=None)
async def get_copies(db: Session = Depends(get_db)) -> dict:
    """
    Endpoint to get all copies for copy.
    """
    logging.info("All Copy Requested")

    data = db.execute(select(Copy)).unique().scalars().all()
    return custom_response(
        status_code=status.HTTP_200_OK, details="Copies found", data=data
    )

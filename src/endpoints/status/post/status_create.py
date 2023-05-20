import logging

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from src.dependencies import get_current_librarian, get_db
from src.endpoints.status.router_init import router
from src.models.status import Status
from src.responses import custom_response
from src.schemas.status import StatusSchema


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=None)
async def status_create(
    status_req: StatusSchema,
    db: Session = Depends(get_db),
    librarian=Depends(get_current_librarian),
) -> dict:
    """
    Creates the Status .
    Params
    ------
    JWT token of librarian.\n
    author_id: int
    Returns
    ------
    Create Status Object
    """
    logging.info(f"Creating status {status_req.status} -- {__name__}")
    status_model = Status()
    status_model.status = status_req.status
    try:
        db.add(status_model)
        db.commit()
        db.refresh(status_model)
        status_req.status_id = status_model.id
        logging.info(f"Created status {status_req.status} -- {__name__}")
        return custom_response(
            status_code=status.HTTP_200_OK, details="Success", data=status_req
        )
    except Exception as e:
        logging.error(f"{e} -- {__name__}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

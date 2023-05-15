from fastapi import Depends
from sqlalchemy.orm import Session
from starlette import status

from src.dependencies import get_db
from src.endpoints.status.router_init import router
from src.models.status import Status
from src.schemas.status import StatusSchema


@router.get("/", status_code=status.HTTP_200_OK, response_model=None)
async def status_create(
    status: StatusSchema,
    db: Session = Depends(get_db),
) -> Status:
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
    status_model = Status(status=status.status)
    try:
        db.commit(status_model)
        db.refresh(status_model)
        return status_model
    except Exception as e:
        raise e

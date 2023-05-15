from typing import List

from fastapi import Depends
from sqlalchemy.orm import Session
from starlette import status

from src.dependencies import get_db
from src.endpoints.status.router_init import router
from src.models.status import Status


@router.get("/", status_code=status.HTTP_200_OK, response_model=None)
async def get_status(db: Session = Depends(get_db)) -> List[Status]:
    statuses = db.execute(Status).scalars().all()
    return statuses

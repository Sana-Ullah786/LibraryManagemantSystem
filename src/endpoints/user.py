from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette import status

from ..models.database import get_db
from ..models.user import User
from ..schemas.user import UserSchema
from .auth import get_current_librarian

router = APIRouter(
    prefix="/user", tags=["user"], responses={401: {"user": "Not authorized"}}
)


@router.get("/", status_code=status.HTTP_200_OK, response_model=None)
def get_all_user(
    librarian: dict = Depends(get_current_librarian), db: Session = Depends(get_db)
) -> List[User]:
    """
    Returns the list of all the users registered in a library.
    Param
    -----
    JWT token of a librarian.
    Throws an exception if JWT is not of librarian
    """
    users = db.execute(select(User).where(True)).scalars().all()
    return users

import logging

from fastapi import Depends, Path
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette import status

from src.dependencies import get_current_librarian, get_db
from src.endpoints.user.router_init import router
from src.exceptions import custom_exception
from src.models.user import User
from src.responses import custom_response


@router.get("/{user_id}", status_code=status.HTTP_200_OK, response_model=None)
async def get_user_by_id(
    librarian: dict = Depends(get_current_librarian),
    db: Session = Depends(get_db),
    user_id: int = Path(gt=0),
) -> dict:
    """
    Returns a single user.\n
    Param
    -----
    user_id: int\n
    JWT token of a librarian.
    Throws an exception if JWT is not of librarian\n
    Returns
    ------
    dict : A dict with status code, details and data
    """
    try:
        user = db.execute(select(User).where(User.id == user_id)).scalars().first()
    except Exception as e:
        logging.exception(f"Exception occured -- {__name__}.get_user_by_id")
        raise custom_exception(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            details=f"Database not available. details: {e}",
        )
    if user:
        logging.info(f"Returning a single user. -- {__name__}.get_user_by_id")
        return custom_response(
            status_code=status.HTTP_200_OK, details="User found", data=user
        )
    else:
        logging.error(f"User not found -- {__name__}.get_user_by_id")
        raise custom_exception(
            status_code=status.HTTP_404_NOT_FOUND, details="User not found."
        )

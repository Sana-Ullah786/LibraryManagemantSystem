import logging

from fastapi import Depends, status
from sqlalchemy.orm import Session

from src.dependencies import get_current_librarian, get_db
from src.endpoints.auth.auth_utils import create_user
from src.endpoints.auth.router_init import router
from src.schemas.user import UserSchemaIn, UserSchemaOut


@router.post(
    "/librarian/register",
    status_code=status.HTTP_201_CREATED,
    response_model=UserSchemaOut,
)
async def create_new_librarian(
    user: UserSchemaIn,
    db: Session = Depends(get_db),
    librarian: dict = Depends(get_current_librarian),
) -> UserSchemaOut:
    """
    Creates a new librarian (requires authentication by another librarian)
    """
    librarian = create_user(user, is_librarian=True, db=db)
    logging.info(f"New Librarian with ID {librarian.id} created.")
    return librarian

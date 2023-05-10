from fastapi import Depends, status
from sqlalchemy.orm import Session

from src.dependencies import get_current_librarian, get_db
from src.endpoints.auth.auth_utils import create_user
from src.endpoints.auth.router_init import router
from src.schemas.user import UserSchema


@router.post("/librarian/register", status_code=status.HTTP_201_CREATED)
async def create_new_librarian(
    user: UserSchema,
    db: Session = Depends(get_db),
    librarian: dict = Depends(get_current_librarian),
) -> dict[str, str]:
    """
    Creates a new librarian (requires authentication by another librarian)
    """
    create_user(user, is_librarian=True, db=db)
    return {"status": "success", "message": "Librarian created"}

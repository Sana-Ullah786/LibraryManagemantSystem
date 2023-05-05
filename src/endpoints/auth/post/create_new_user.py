from fastapi import Depends, status
from sqlalchemy.orm import Session

from src.dependencies import get_db
from src.endpoints.auth.auth_utils import create_user
from src.endpoints.auth.router_init import router
from src.schemas.user import UserSchema


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def create_new_user(
    user: UserSchema, db: Session = Depends(get_db)
) -> dict[str, str]:
    """
    Creates a new user
    """
    create_user(user, is_librarian=False, db=db)
    return {"status": "success", "message": "User created"}

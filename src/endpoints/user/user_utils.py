import logging

from sqlalchemy import and_, select
from sqlalchemy.orm import Session

from src.dependencies import get_password_hash
from src.endpoints.user.exceptions import user_not_exist
from src.models.user import User
from src.responses import custom_response
from src.schemas.update_user import UpdateUserSchema
from src.schemas.user import UserSchemaOut


def update_user(new_user: UpdateUserSchema, user_id: int, db: Session) -> dict:
    """
    Updates the db with new user data.\n
    Params
    ------
    new_user: New user data
    user_id: int id of the user to update the data of.
    """
    current_user = db.scalar(
        select(User).where(and_(User.id == user_id, User.is_deleted is False))
    )
    if not current_user:
        raise user_not_exist()
    current_user.email = new_user.email
    current_user.username = new_user.username
    current_user.password = get_password_hash(new_user.password)
    current_user.first_name = new_user.first_name
    current_user.last_name = new_user.last_name
    current_user.contact_number = new_user.contact_number
    current_user.address = new_user.address
    logging.info(f"Updating user {user_id} -- {__name__}.udpate_current_user")
    db.commit()
    new_user = UserSchemaOut(**current_user.__dict__)
    return custom_response(status_code=200, details="User updated", data=new_user)

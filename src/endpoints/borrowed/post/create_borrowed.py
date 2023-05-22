import logging

from fastapi import Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.dependencies import get_current_user, get_db
from src.endpoints.borrowed.router_init import router
from src.exceptions import custom_exception
from src.models import all_models
from src.responses import custom_response
from src.schemas.borrowed import BorrowedSchema
from src.status_constants import AVAILABLE, BORROWED


@router.post("/", response_model=None, status_code=status.HTTP_201_CREATED)
async def create_borrowed(
    borrowed: BorrowedSchema,
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict:
    """
    This function will be used to create a new borrowed.
    Parameters:
        borrowed: The borrowed data.
        db: The database session.
    Returns:
        A dictionary containing the status code, details and data.
    """
    logging.info(f"Creating new borrowed in database with user ID: {user.get('id')}")
    copy = (
        db.scalars(
            select(all_models.Copy).where(all_models.Copy.id == borrowed.copy_id)
        )
        .unique()
        .one_or_none()
    )
    if copy is None:
        raise custom_exception(
            status_code=status.HTTP_400_BAD_REQUEST,
            details="Copy with given ID does not exist",
        )
    found_status = (
        db.scalars(
            select(all_models.Status).where(all_models.Status.id == copy.status_id)
        )
        .unique()
        .one_or_none()
    )
    if found_status is None:
        raise custom_exception(
            status_code=status.HTTP_400_BAD_REQUEST,
            details="Status with given ID does not exist",
        )
    if found_status.status != AVAILABLE:
        raise custom_exception(
            status_code=status.HTTP_400_BAD_REQUEST, details="Copy is not available"
        )
    try:
        new_status_id = db.scalars(
            select(all_models.Status.id).where(all_models.Status.status == BORROWED)
        ).first()
        copy.status_id = new_status_id
        new_borrowed = all_models.Borrowed()
        new_borrowed.copy_id = borrowed.copy_id
        new_borrowed.user_id = user.get("id")
        new_borrowed.issue_date = borrowed.issue_date
        new_borrowed.due_date = borrowed.due_date
        new_borrowed.return_date = borrowed.return_date
        db.add(new_borrowed)
        db.commit()
        logging.info(f"Created new borrowed in database with user ID: {user.get('id')}")
        db.refresh(new_borrowed)
        borrowed.id = new_borrowed.id
        borrowed.user_id = user.get("id")
        return custom_response(
            status_code=status.HTTP_201_CREATED,
            details="Borrowed created successfully!",
            data=borrowed,
        )
    except Exception as e:
        logging.exception(
            "Error getting all borroweds from database. Details = " + str(e)
        )
        raise custom_exception(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            details="Error creating borrowed details  = " + str(e),
        )

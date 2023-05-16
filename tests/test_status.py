import logging
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import sessionmaker
from starlette import status

from src.dependencies import get_password_hash
from src.models import all_models
from src.models.all_models import Status
from tests.client import client
from tests.utils import SUPER_USER_CRED  # isort skip
from tests.utils import check_no_auth  # isort skip
from tests.utils import get_fresh_token  # isort skip


def status_create(statusname: str, test_db: sessionmaker) -> None:
    """
    This function will be used to create a user using model.
    Parameters:
        test_db: The database session.
        librarian: The user is librarian or not.
    Returns:
        None
    """
    logging.info("Creating user in database in Test DB")
    status_model = Status(status=statusname)

    with test_db() as db:
        db.add(status_model)
        db.commit()
        db.refresh(status_model)
    logging.info("Created user in database in Test DB with id: " + str(status_model.id))

from typing import Generator

import pytest
from sqlalchemy.orm import sessionmaker

from src.models.all_models import Base

from .client import TestingSessionLocal, engine


@pytest.fixture()
def test_db() -> Generator[sessionmaker, None, None]:
    """
    A fixture function that is to be injected as a dependency in all tests. It creates tables for all models in the test database and yields a test database session maker. After the tests conclude it cleans up the test database
    """
    Base.metadata.create_all(bind=engine)
    yield TestingSessionLocal
    Base.metadata.drop_all(bind=engine)

from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

SQLALCHEMY_DATABASE_URL = (
    "postgresql+psycopg2://mustansir:12345678@localhost/library_management"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """
    A generetor function that yields the DB session
    """
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

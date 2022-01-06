import os
from typing import TYPE_CHECKING, Any, Dict

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

if TYPE_CHECKING:
    from sqlalchemy.orm import Session

# "postgresql://user:password@postgresserver/db"
SQLALCHEMY_DATABASE_URL: str = os.getenv(
    "DATABASE_URL",
    "sqlite:///froidapi.db"
)
"""
Database URL for SQLAlchemy to connect to. 
It can be retrieved from the environment variable `DATABASE_URL` or
it can be set manually.
"""
LOCAL_DB: bool = "sqlite" in SQLALCHEMY_DATABASE_URL
"""Wheter the database is local or remote. If it is local,
then add `check_same_thread` to the sessionmaker.
"""

# If we are using sqlite, we need to add `check_same_thread` to the sessionmaker.
engine_kwargs: Dict[str, Any] = {} if not LOCAL_DB else {"check_same_thread": False}
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    # If we're using SQLite, we need to specify the below option.
    connect_args=engine_kwargs,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
"""Session factory for SQLAlchemy, which is used to create a session."""
Base = declarative_base()
"""Base class for all models."""


# get db session
def get_session() -> "Session":
    sess = SessionLocal()
    try:
        yield sess
    finally:
        sess.close()


def init_db() -> None:
    """Create the database and tables."""
    Base.metadata.create_all(bind=engine)


def drop_db() -> None:
    """Drop the database tables."""
    Base.metadata.drop_all(bind=engine)

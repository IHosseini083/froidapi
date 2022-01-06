from typing import TYPE_CHECKING, List, Optional

if TYPE_CHECKING:
    from sqlalchemy.orm import Session

from passlib.context import CryptContext

from . import models, schemas
from .exceptions import (
    AuthenticationError,
    OldCredentialsError,
    TokenNotFoundError,
    UserNotFoundError
)

# install passlib[bcrypt] module first
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash user password with `bcrypt` algorithm and return the hash."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify that a plain text password matches a hash."""
    return pwd_context.verify(plain_password, hashed_password)


def authenticate_user(db: "Session", username: str, password: str) -> models.User:
    """Authenticate a user by username and password.

    Parameters:
        db (:class:`sqlalchemy.orm.Session`): Database session.
        username (`str`): Username of the user.
        password (`str`): Password of the user.

    Returns:
        :class:`database.models.User`: Authenticated user.

    Raises:
        :class:`database.exceptions.AuthenticationError`: If authentication fails.
        :class:`database.exceptions.UserNotFoundError`: If user is not found.
    """
    user = get_user_by_username(db, username)
    if not user:
        raise UserNotFoundError(f"User with username {username!r} not found.")
    if not verify_password(password, user.hashed_password):
        raise AuthenticationError("Invalid credentials.")
    return user


def get_user_by_email(db: "Session", email: str) -> Optional["models.User"]:
    """Get a user from the database by email."""
    return db.query(models.User).filter(models.User.email == email).first()


def get_user_by_username(db: "Session", username: str) -> Optional["models.User"]:
    """Get a user from the database by username."""
    return db.query(models.User).filter(models.User.username == username).first()


def get_users(db: "Session", skip: int = 0, limit: int = 100) -> List["models.User"]:
    """Get all users from the database.

    Parameters:
        db (:class:`sqlalchemy.orm.Session`): Database session.
        skip (`int`): Number of users to skip from the beginning.
        limit (`int`): Maximum number of users to return.

    Returns:
        `list` of :class:`database.models.User`: A list of users.
    """
    return db.query(models.User).offset(skip).limit(limit).all()


def save_user(db: "Session", user: schemas.UserCreate) -> models.User:
    """Save a user in the database.

    Parameters:
        db (:class:`sqlalchemy.orm.Session`): Database session.
        user (:class:`database.schemas.UserCreate`): User to create.

    Returns:
        :class:`database.models.User`: Created user.
    """
    to_save = user.dict()
    to_save["hashed_password"] = hash_password(to_save.pop("password"))
    db_user = models.User(**to_save)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: "Session", user: models.User) -> models.User:
    """Delete a user from the database."""
    db.delete(user)
    db.commit()
    return user


def update_user_password(db: "Session", user: models.User, new_password: str) -> models.User:
    """Update a user's password in the database."""
    if verify_password(new_password, user.hashed_password):
        raise OldCredentialsError(
            "New password must be different than old password."
        )
    user.hashed_password = hash_password(new_password)
    db.commit()
    db.refresh(user)
    return user


def create_token(db: "Session", user: models.User) -> models.Token:
    """Create a new token for a user."""
    token_string = models.Token.generate_token_string()
    token = models.Token(token=token_string, user_id=user.id)
    db.add(token)
    db.commit()
    db.refresh(token)
    return token


def revoke_token(db: "Session", user: models.User) -> models.Token:
    """Revoke a user's token."""
    if not user.token:
        raise TokenNotFoundError(
            f"Could not find any token for user {user.username!r} "
            "to revoke."
        )
    user_token = user.token
    db.delete(user_token)
    db.commit()
    db.refresh(user)
    return user_token


def verify_token(db: "Session", token_string: str) -> models.Token:
    """Verify that a token is valid."""
    token = db.query(models.Token).filter(models.Token.token == token_string).first()
    if not token:
        raise TokenNotFoundError(f"Token {token_string!r} not found.")
    return token

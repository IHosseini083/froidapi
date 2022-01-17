from database import models, schemas
from database import utils as db_utils
from database.db import get_session
from database.exceptions import (
    AuthenticationError,
    OldCredentialsError,
    TokenNotFoundError,
    UserNotFoundError
)
from fastapi import APIRouter, Body, Depends
from sqlalchemy.orm import Session

from .base import raise_error
from .models import UserCredentials

# TODO: exclude user endpoints from docs
router = APIRouter(
    tags=["Users"],
    prefix="/users",
    responses={
        204: {"description": "No content, operation successful."},
        401: {"description": "Unauthorized, invalid credentials."},
    }
)


def get_user_cred(
    user: UserCredentials = Body(
        ...,
        title="User Credentials",
        description="User credentials for authentication.",
        example={"username": "Reza", "password": "some_strong_password"}
    )
) -> UserCredentials:
    """Return the user credentials from the request."""
    return user


def user_auth_handler(db: Session, user: UserCredentials) -> models.User:
    """Authenticate a user by username and password and return the user."""
    try:
        db_user = db_utils.authenticate_user(db, user.username, user.password)
    except AuthenticationError as e:
        raise_error(401, message=str(e))
    except UserNotFoundError as e:
        raise_error(404, message=str(e))
    else:
        return db_user


# Because we are using SQLAlchemy as db, we should use
# normal path functions instead of async functions.
@router.post(
    "/register",
    response_model=schemas.RegisteredUser,
    summary="User registration",
    response_description="The user that was registered.",
    status_code=201
)
def register_user(
    user: schemas.UserCreate = Body(
        ...,
        title="User registration data",
        description="The data to register a new user. "
    ),
    db: "Session" = Depends(get_session)
) -> models.User:
    db_user = db_utils.get_user_by_username(db, user.username)
    if db_user:
        raise_error(400, message="User with this username already exists.")
    return db_utils.save_user(db, user)


@router.post(
    "/me",
    response_model=schemas.RegisteredUser,
    summary="Get user's profile",
    response_description="The user's profile data.",
    status_code=200
)
def get_me(
    user: UserCredentials = Depends(get_user_cred),
    db: "Session" = Depends(get_session)
) -> models.User:
    return user_auth_handler(db, user)


@router.delete(
    "/me",
    response_model=None,
    summary="Delete user's profile",
    status_code=204
)
def delete_me(
    user: UserCredentials = Depends(get_user_cred),
    db: "Session" = Depends(get_session)
) -> None:
    db_user = user_auth_handler(db, user)
    db_utils.delete_user(db, db_user)


@router.put(
    "/me/change-password",
    response_model=schemas.RegisteredUser,
    summary="Change user's password",
    response_description="The user's profile data.",
    status_code=200
)
def update_me(
    new_password: str = Body(
        ...,
        title="New password",
        description=(
            "The new password for the user. "
            "Must be at least 8 characters long and "
            "different from the old password."
        ),
        example="new_pass_8000",
        min_length=8
    ),
    user: UserCredentials = Depends(get_user_cred),
    db: "Session" = Depends(get_session)
) -> models.User:
    db_user = user_auth_handler(db, user)
    try:
        return db_utils.update_user_password(db, db_user, new_password)
    except OldCredentialsError as e:
        raise_error(400, message=str(e))


# get user's token
@router.post(
    "/me/token",
    response_model=schemas.UserToken,
    summary="Get user's token.",
    response_description="The user's token data.",
    status_code=200
)
def get_token(
    user: UserCredentials = Depends(get_user_cred),
    db: "Session" = Depends(get_session)
) -> models.Token:
    db_user = user_auth_handler(db, user)
    if not db_user.token:
        raise_error(404, message=f"User {user.username!r} has no token.")
    return db_user.token


# create a token for the user
@router.post(
    "/me/token/new",
    response_model=schemas.UserToken,
    summary="Create a new token for the user.",
    response_description="The generated token.",
    status_code=201
)
def create_token(
    user: UserCredentials = Depends(get_user_cred),
    db: "Session" = Depends(get_session)
) -> models.Token:
    db_user = user_auth_handler(db, user)
    if db_user.token:
        raise_error(400, message=f"User {user.username!r} already has a token.")
    return db_utils.create_token(db, db_user)


# delete user's token
@router.delete(
    "/me/token/revoke",
    response_model=None,
    summary="Revoke the user's token.",
    status_code=204
)
def revoke_token(
    user: UserCredentials = Depends(get_user_cred),
    db: "Session" = Depends(get_session)
) -> None:
    db_user = user_auth_handler(db, user)
    try:
        db_utils.revoke_token(db, db_user)
    except TokenNotFoundError:
        raise_error(
            404,
            message=f"User {user.username!r} does not have any token to revoke."
        )

import typing as t
from datetime import datetime as dt

from pydantic import BaseModel, EmailStr, Field


class UserToken(BaseModel):
    """Model for users' token in the database."""
    id: int = Field(
        ...,
        title="Token ID",
        description="Unique identifier for the token in the database.",
        example=32,
        gt=0
    )
    token: str = Field(
        ...,
        title="Token",
        description="Unique token for the user.",
        example="some_long_token_string"
    )
    user_id: int = Field(
        ...,
        title="User ID",
        description="Unique identifier for the user.",
        example=32,
        gt=0
    )
    created_at: dt = Field(
        ...,
        title="Creation datetime",
        description="Exact datetime of the token creation.",
        example="2022-01-06T23:04:17.073179"
    )

    class Config:
        orm_mode = True


class BaseUser(BaseModel):
    """Base model for user data"""
    username: str = Field(
        ...,
        title="Username",
        description=(
            "The username of the user. "
            "Must be unique and can only contain letters, "
            "numbers, and underscores."
        ),
        example="Reza",
        min_length=3,
        max_length=20
    )
    email: EmailStr = Field(
        ...,
        title="Email",
        description=(
            "User's email address. "
            "Must be unique and valid email address"
        ),
        example="info@example.com"
    )


class UserCreate(BaseUser):
    """Model for user creation"""
    password: str = Field(
        ...,
        title="Password",
        description=(
            "The password of the user. "
            "Must be at least 8 characters long and "
            "do not contain spaces."
        ),
        min_length=8,
        max_length=32,
        regex="^[^ ]+$",
        example="some_strong_password"
    )


class RegisteredUser(BaseUser):
    """Model for registered users."""
    hashed_password: str = Field(
        ...,
        title="Hashed password",
        description=(
            "User's hashed password using bcrypt algorithm. "
            "This is used to authenticate the user."
        )
    )
    created_at: dt = Field(
        ...,
        title="Creation datetime",
        description="Exact datetime of the user creation.",
        example="2022-01-05T16:22:51.311046"
    )
    token: t.Optional["UserToken"] = Field(
        None,
        title="User token",
        description=(
            "User's token (if any). "
            "It's a JSON object with the following fields: "
            "`id`, `token`, `user_id` and `created_at`."
        )
    )

    class Config:
        orm_mode = True

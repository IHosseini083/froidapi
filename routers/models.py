from pydantic import AnyUrl, BaseModel, EmailStr, Field


class BaseUser(BaseModel):
    """Base model for user data"""
    username: str = Field(
        ..., 
        description=(
            "The username of the user. "
            "Must be unique and can only contain letters, "
            "numbers, and underscores."
        ),
        example="Reza",
        min_length=3,
        max_length=20,
        regex=r"^[a-zA-Z0-9_]{3,20}$"
    )
    email: EmailStr = Field(
        ...,
        description=(
            "User's email address. "
            "Must be unique and valid email address like "
            "'example@domain.com'."
        ),
        example="example@domain.com"
    )


class UserRegister(BaseUser):
    """Model for user registration"""
    password: str = Field(
        ...,
        description=(
            "User's password. "
            "Must be at least 8 characters long and "
            "consist of letters, numbers, and other "
            "characters."
        ),
        example="strong_password",
        min_length=8,
    )


class RegisteredUser(BaseUser):
    """Model for registered users."""


class SearchResult(BaseModel):
    """Model for search result."""
    id: int = Field(
        ...,
        description=(
            "The unique identifier of the post. "
            "This is used to identify the post in the farsroid website."
        ),
        example=12350
    )
    title: str = Field(
        ...,
        description="The title of the post.",
        example="clash of clans",
        min_length=3
    )
    url: AnyUrl = Field(
        ...,
        description="The URL of the post.",
        example="https://www.farsroid.com/clash-of-clans/"
    )

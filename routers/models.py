from typing import List

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


class SearchItem(BaseModel):
    """Model for search result items (applications)."""
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


class PaginatedResult(BaseModel):
    """
    Model for paginated results that contain page number
    and number of items per page (e.g. search result, comments).
    """
    page: int = Field(
        ...,
        description="The page number of the result.",
        example=1,
        gt=0
    )
    per_page: int = Field(
        ...,
        description="The number of items per page.",
        example=10,
        gt=0
    )
    items: List = Field(
        ...,
        description="The list of items in the result.",
        example=[
            {
                "id": 12350,
                "title": "clash of clans",
                "url": "https://www.farsroid.com/clash-of-clans/"
            }
        ],
        max_items=100,
    )


class PostStatistics(BaseModel):
    """Model for a posts' statistics. (e.g. views, likes, etc.)"""
    post_id: int = Field(
        ...,
        description=(
            "The unique identifier of the post."
        ),
        example=10555,
        gt=0
    )
    likes: int = Field(
        ...,
        description="The number of likes for the post.",
        example=7023
    )
    total_downloads: int = Field(
        ...,
        description="The number of downloads for the post.",
        example=113324
    )
    monthly_downloads: int = Field(
        ...,
        description="The number of monthly downloads for the post.",
        example=234
    )
    weekly_downloads: int = Field(
        ...,
        description="The number of weekly downloads for the post.",
        example=23
    )
    today_downloads: int = Field(
        ...,
        description="The number of times the post was downloaded today.",
        example=2
    )
    views: int = Field(
        ...,
        description="The number of views for the post.",
        example=2147472
    )


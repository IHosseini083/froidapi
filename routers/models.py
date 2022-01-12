import typing as t

from pydantic import BaseModel, Field, HttpUrl


class UserCredentials(BaseModel):
    """User's credentials for authentication purposes."""
    username: str = Field(
        ...,
        title="Username",
        description="The username of the user.",
        example="Reza",
        min_length=3,
        max_length=20
    )
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
        # password must not contain spaces
        regex="^[^ ]+$",
        example="some_strong_password"
    )


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
    url: HttpUrl = Field(
        ...,
        description="The URL of the post.",
        example="https://www.farsroid.com/clash-of-clans/"
    )


class PaginatedResult(BaseModel):
    """
    Model for paginated results that contain page number
    and number of items per page (e.g. search result, comments).
    """
    total_pages: t.Optional[int] = Field(
        None,
        title="Total Pages",
        description="The total number of pages available for the result.",
    )
    page: int = Field(
        ...,
        title="Page",
        description="The current page number.",
        example=1,
        gt=0
    )
    items_count: int = Field(
        ...,
        title="Items Count",
        description="The number of items returned in the result.",
        example=1
    )
    items: t.List = Field(
        ...,
        title="Items",
        description="An array of items returned in the result.",
        max_items=100
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

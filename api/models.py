from typing import List, Optional

from pydantic import BaseModel, Field, HttpUrl


class Comment(BaseModel):
    """Represents a comment on a post."""
    comment_id: int = Field(
        ...,
        title="Comment ID",
        description="The ID of the comment.",
        example=1837937
    )
    post_id: int = Field(
        ...,
        title="Post ID",
        description="The ID of the post this comment is on.",
        example=12355,
    )
    content: str = Field(
        ...,
        title="Content",
        description="The content of the comment in plain text.",
        example="This is a comment.",
    )
    link: HttpUrl = Field(
        ...,
        title="Link",
        description="The link to the comment on that post.",
        example="https://www.farsroid.com/combat-magic/comment-page-2/#comment-1837937"
    )
    date: str = Field(
        ...,
        title="Date",
        description="The date the comment was posted.",
        example="2021-08-13T22:46:44"
    )
    author: str = Field(
        ...,
        title="Author",
        description="The name of the author of the comment.",
        example="علی"
    )
    parent_id: Optional[int] = Field(
        None,
        title="Parent ID",
        description="The ID of the parent comment (the comment that this comment is a reply to).",
        example=1837937
    )

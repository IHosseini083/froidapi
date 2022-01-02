from enum import Enum
from typing import Dict, List, Optional

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


class DownloadData(BaseModel):
    """Represents the data to download a file from a URL."""
    title: str = Field(
        ...,
        title="Title",
        description="The title of the download link.",
        example="دانلود فایل نصبی اصلی بازی با لینک مستقیم- 177 مگابایت"
    )
    url: HttpUrl = Field(
        ...,
        title="URL",
        description="The URL to download the file from.",
        example="https://www.dl.farsroid.com/game/Asphalt-8-6.1.0g(Farsroid.com).apk"
    )


class PostMedia(BaseModel):
    """Represents a post's media (video, etc.)."""
    url: HttpUrl = Field(
        ...,
        title="URL",
        description="The URL to the media.",
        example="https://www.farsroid.com/wp-content/uploads/Asphalt-8-Airborne-logo-3-1.jpg"
    )
    media_type: str = Field(
        ...,
        title="Media Type",
        description="The type of media.",
        example="thumbnail"
    )


class RelatedPost(BaseModel):
    """Represents a related post."""
    post_id: int = Field(
        ...,
        title="Post ID",
        description="The ID of the related post.",
        example=12355
    )
    title: str = Field(
        ...,
        title="Title",
        description="The title of the related post.",
        example="Asphalt 8 Airborne"
    )
    url: HttpUrl = Field(
        ...,
        title="URL",
        description="The URL to the related post.",
        example="https://www.farsroid.com/?p=12355"
    )
    thumbnail: HttpUrl = Field(
        ...,
        title="Thumbnail URL",
        description="The URL to the thumbnail of the related post.",
        example="https://www.farsroid.com/wp-content/uploads/Asphalt-8-Airborne-logo-3-1.jpg"
    )


class PostDownloadPgae(BaseModel):
    """Represents a post's download page."""
    post_id: int = Field(
        ...,
        title="Post ID",
        description="The ID of the post.",
        example=12355,
    )
    title: str = Field(
        ...,
        title="Title",
        description="The title of the post.",
        example="دانلود Asphalt 8 Racing Game 6.1.0g – آخرین ورژن بازی آسفالت 8 اندروید + مود"
    )
    description: str = Field(
        ...,
        title="Description",
        description="The description of the post.",
        example=(
            "...جدیدترین ورژن بازی آسفالت 8 آندروید نسخه معمولی + نسخه مود "
            "(پول بی نهایت) به صورت جداگانه تست شده با اجرای بدون مشکل پیشنهاد ویژه"
        )
    )
    post_url: HttpUrl = Field(
        ...,
        title="Post URL",
        description="The URL of the post on the site.",
        example="https://www.farsroid.com/?p=12355"
    )
    media: List[PostMedia] = Field(
        ...,
        title="Media",
        description="The media (video, etc.) of the post from the site.",
        example=[
            {
                "url": "https://www.farsroid.com/wp-content/uploads/Asphalt-8-Airborne-logo-3-1.jpg",
                "media_type": "thumbnail"
            }
        ]
    )
    meta: Dict[str, str] = Field(
        ...,
        title="Meta",
        description="The meta data of the post.",
        example={
            "version": "6.1.0",
            "mode": "offline",
            "required_android_version": "5.0",
            # TODO: add support for categories
            "category": "Games",
        }
    )
    download_data: Optional[List[DownloadData]] = Field(
        None,
        title="Download Data",
        description="The data to download the post from the site.",
        example=[
            {
                "url": "https://www.dl.farsroid.com/game/Asphalt-8-6.1.0g(Farsroid.com).apk",
                "filename": "دانلود فایل نصبی اصلی بازی با لینک مستقیم- 177 مگابایت"
            }
        ]
    )
    related_posts: Optional[List[RelatedPost]] = Field(
        None,
        title="Related Posts",
        description="The IDs of the posts that are related/similar to this post.",
        example={
            "post_id": 12355,
            "title": "Asphalt 8 Airborne",
            "url": "https://www.farsroid.com/?p=12355",
            "thumbnail": "https://www.farsroid.com/wp-content/uploads/Asphalt-8-Airborne-logo-3-1.jpg"
        }
    )
    gplay_url: Optional[HttpUrl] = Field(
        None,
        title="Google Play URL",
        description="The URL to the post on Google Play.",
        example="https://play.google.com/store/apps/details?id=com.gameloft.android.ANMP.GloftA8HM"
    )

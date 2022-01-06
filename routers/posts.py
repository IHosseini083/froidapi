from enum import Enum
from typing import List, Optional

from api.exceptions import BadRequestError, NotFoundError
from api.models import Comment, PostDownloadPgae
from fastapi import APIRouter, Query

from .base import api_handler, raise_error
from .models import PaginatedResult, PostStatistics, SearchItem
from .utils import decode_html_entities

router = APIRouter(tags=["Posts"], prefix="/posts")


########## Enums ##########
class CommentsOrder(str, Enum):
    """Order comments in `asceding` or `descending` order."""

    ASC = "asc"
    DESC = "desc"


class CommentsOrderBy(str, Enum):
    """Order comments by different fields (e.g. `date`)."""

    DATE = "date"
    DATE_GMT = "date_gmt"
    ID = "id"


########## Routes ##########
@router.get(
    "/search",
    response_model=PaginatedResult,
    summary="Search for a post on farsroid.com.",
    response_description="The search results.",
    status_code=200
)
async def search(
        query: str = Query(
            ...,
            title="Query",
            description="The query to search for.",
            min_length=3,
            example="clash of clans",
            alias="q"
        ),
        page: Optional[int] = Query(
            None,
            title="Page",
            description="The page number to fetch. Default is 1.",
            gt=0
        ),
        per_page: Optional[int] = Query(
            None,
            title="Per Page",
            description=(
                "The number of results per page. "
                "If not specified, the default is 10 results per page. "
                "The maximum is 100 results per page."
            ),
            gt=0
        )
) -> PaginatedResult:
    res = await api_handler.search(query, page, per_page)
    items = [
        SearchItem(
            id=item["id"],
            title=decode_html_entities(item["title"]),
            url=item["url"]
        )
        for item in res
    ]
    return PaginatedResult(
        page=page or 1,  # Default page is 1
        items_count=len(items),
        items=items
    )


@router.get(
    "/{post_id}/dp",
    response_model=PostDownloadPgae,
    summary="Get a post's download page (dp) by its ID.",
    response_description="The post's download page data.",
    status_code=200
)
async def get_post(
        post_id: int = Query(
            ...,
            title="Post ID",
            description="The ID of the post to fetch.",
            example=10555,
            gt=0
        )
) -> PostDownloadPgae:
    try:
        return await api_handler.get_post(post_id)
    except NotFoundError:
        raise_error(404, message=f"post {post_id} not found")


@router.get(
    "/{post_id}/stats",
    response_model=PostStatistics,
    summary="Get statistics for a post stored on farsroid.com database.",
    response_description="The statistics for the post such as downloads, views, etc.",
    status_code=200
)
async def get_post_statistics(
        post_id: int = Query(
            ...,
            title="Post ID",
            description=(
                "The ID of the post to get statistics for. "
                "This can be found in search results."
            ),
            example=10555,
            gt=0
        )
) -> PostStatistics:
    try:
        res = await api_handler.get_post_statistics(post_id)
        # farsroid API returns 400 if the post is not found!
    except (BadRequestError, NotFoundError):
        res = None
    if not res:
        # TODO: extend the error details (e.g. the post ID, status code, etc.)
        raise_error(404, message=f"post {post_id} not found")
    data = res["data"][0]
    return PostStatistics(
        post_id=data["post_id"],
        views=data["views"],
        likes=data["likes"],
        total_downloads=data["download"],
        monthly_downloads=data["download_month"],
        weekly_downloads=data["download_week"],
        today_downloads=data["download_today"]
    )


@router.get(
    "/{post_id}/comments",
    response_model=List[Comment],
    summary="Get the comments that were made on a post (approved ones).",
    response_description="The list of comments.",
    status_code=200
)
async def get_post_comments(
        post_id: int = Query(
            ...,
            title="Post ID",
            description=(
                "The ID of the post to get comments for. "
                "This can be found in search results."
            ),
            example=10555,
            gt=0
        ),
        page: int = Query(
            1,
            title="Page",
            description="The page number to fetch.",
            gt=0,
            lt=101
        ),
        per_page: int = Query(
            10,
            title="Per Page",
            description="The number of results per page.",
            gt=0,
            lt=101
        ),
        search: Optional[str] = Query(
            None,
            title="Search",
            description="The search query to filter comments by.",
            min_length=3,
        ),
        order: Optional[CommentsOrder] = Query(
            None,
            title="Order",
            description="The order to fetch comments in.",
            example="desc"
        ),
        order_by: Optional[CommentsOrderBy] = Query(
            None,
            title="Order By",
            description="The field to order comments by.",
            example="date_gmt"
        )
) -> List[Comment]:
    # TODO: add pagination and sorting of comments => DONE
    try:
        return await api_handler.get_comments_by(
            "post",
            post_id,
            page=page,
            per_page=per_page,
            search=search,
            order_by=order_by.value if order_by else None,
            order=order.value if order else None
        )
    except (BadRequestError, NotFoundError):
        raise_error(404, message=f"post {post_id} not found")

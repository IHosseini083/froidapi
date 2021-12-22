from typing import Optional

from fastapi import APIRouter, Query

from api.exceptions import NotFoundError
from .base import api_handler
from .models import PaginatedResult, PostStatistics, SearchItem
from .utils import decode_html_entities

router = APIRouter(
    tags=["Posts"],
    prefix="/posts",
    responses={
        400: {"description": "Bad request, invalid parameters were sent."},
    }
)


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
            description="The page number to fetch.",
            gt=0
        ),
        per_page: Optional[int] = Query(
            None,
            title="Per Page",
            description="The number of results per page.",
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
        page=page or 1,
        per_page=per_page or 10,
        items=items
    )


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
    res = await api_handler.get_post_statistics(post_id)
    data = res["data"][0]
    if not data:
        raise NotFoundError(msg=f"post {post_id!r} not found", code=404)
    return PostStatistics(
        post_id=data["post_id"],
        views=data["views"],
        likes=data["likes"],
        total_downloads=data["download"],
        monthly_downloads=data["download_month"],
        weekly_downloads=data["download_week"],
        today_downloads=data["download_today"]
    )

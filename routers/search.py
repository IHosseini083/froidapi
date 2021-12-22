from typing import List, Optional

from fastapi import APIRouter, Query

from .base import api_handler
from .models import SearchResult
from .utils import decode_html_entities

router = APIRouter()


@router.get(
    "/",
    response_model=List[SearchResult],
    summary="Search for a post (application) on farsroid.com.",
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
) -> List[SearchResult]:
    res = await api_handler.search(query, page, per_page)
    return [
        SearchResult(
            id=r["id"],
            title=decode_html_entities(r["title"]),
            url=r["url"],
        )
        for r in res
    ]

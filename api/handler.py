from typing import TYPE_CHECKING, Any, Dict, List, Optional
from urllib.parse import urlencode

if TYPE_CHECKING:
    from aiohttp import ClientSession

from .sess import Session


class APIHandler:
    """A handler for API calls and responses."""

    __slots__ = ("_sess", )

    def __init__(self, session: "ClientSession", html_parser: Optional[str] = None) -> None:
        self._sess = Session(session, html_parser)

    async def close(self) -> None:
        """Close the session."""
        await self._sess.close()

    async def search(
        self, 
        query: str, 
        page: Optional[int] = None,
        per_page: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Search for a post (application) on farsroid.com.

        Parameters:
            query (`str`): The query to search for.
            page (`int`, optional): The page number to fetch.
            per_page (`int`, optional): The number of results per page.

        Returns:
            `List[Dict[str, Any]]`: A list of search results.
        """
        params = {"search": query, "page": page, "per_page": per_page}
        endpoint = f"/wp-json/wp/v2/search?{urlencode({k: v for k, v in params.items() if v})}"
        return await self._sess.get_json(endpoint)

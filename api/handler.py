from typing import TYPE_CHECKING, Any, Dict, List, Optional, Tuple, Union
from urllib.parse import urlencode

if TYPE_CHECKING:
    from aiohttp import ClientSession
    from .models import PostDownloadPage

from .exceptions import BadRequestError
from .models import Comment, LegacySearchItem
from .parsers import LegacySearchParser, PostParser
from .sess import Session
from .utils import render_content


class APIHandler:
    """A handler for API calls and responses."""

    __slots__ = ("_sess",)

    def __init__(self, session: "ClientSession", html_parser: Optional[str] = None) -> None:
        self._sess = Session(session, html_parser)

    def __enter__(self) -> "APIHandler":
        return self

    async def __aenter__(self) -> "APIHandler":
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        await self.close()

    async def close(self) -> None:
        """Close the API session."""
        await self._sess.close()

    async def legacy_search(self, query: str, page: Optional[int] = None) -> Tuple[List[LegacySearchItem], int]:
        """
        Search for posts only by scraping the page and not using the farsroid `JSON`
        API. This type of searching has low performance and is not recommended but
        can be useful for some users to get more info from search results. 
        (e.g. post thumbnail, description, etc.)

        Parameters:
            query (`str`): The query to search for.
            page (`int`, optional): The page number to fetch.

        Returns:
            A tuple of a list of :class:`LegacySearchItem` objects 
            and the total number of available pages for the search query.
        """
        page_num = page or 1
        if page_num > 1:
            endpoint = f"page/{page_num}/?s={query}"
        else:
            endpoint = f"?s={query}"
        parser = LegacySearchParser(await self._sess.get_soup(endpoint))
        return parser.parsed(), parser.total_pages
    
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
            A tuple of a list of :class:`LegacySearchItem` objects and 
            the total number of available pages for the search query if `legacy` mode is enabled 
            or a list of :class:`Dict[str, Any]` objects if not using the legacy search.
        """
        params = {"search": query, "page": page, "per_page": per_page}
        # make sure to remove None values from params
        endpoint = f"/wp-json/wp/v2/search?{urlencode({k: v for k, v in params.items() if v})}"
        return await self._sess.get_json(endpoint)

    async def get_post_statistics(self, post_id: Union[int, List[int]]) -> Dict[str, Any]:
        """Get statistics for a post (application)

        Parameters:
            post_id (`int` or `List[int]`): The post ID or list of post IDs to get statistics for.

        Returns:
            `Dict[str, Any]`: A dictionary of post statistics.
        """
        ids = post_id if isinstance(post_id, list) else [post_id]
        endpoint = f"/api/posts/?ids={','.join(map(str, ids))}"
        return await self._sess.get_json(endpoint)

    async def get_comments_by(self, by: str, _id: int, **kwargs) -> List["Comment"]:
        """Get comments by post id, parent id or comment id.

        Parameters:
            by (`str`): The type of ID to get comments by (`post`, `parent` or `comment`).
            _id (`int`): The post, parent or comment ID to get comments by.
            **kwargs: Additional keyword arguments to pass to the API call.

        Returns:
            `List[Comment]`: A list of :class:`Comment` objects.
        """
        if by not in ["post", "parent", "comment"]:
            raise BadRequestError(f"Invalid value for `by`: {by!r}", 400)
        if not isinstance(_id, int):
            raise BadRequestError("Invalid data type for `id`", 400)

        query = urlencode({by: _id, **{k: v for k, v in kwargs.items() if v}})
        endpoint = "/wp-json/wp/v2/comments"

        if by != "comment":
            endpoint += f"?{query}"
        else:
            endpoint += f"/{_id}"

        comments: List[Dict[str, Any]] = await self._sess.get_json(endpoint)
        return [
            Comment(
                comment_id=comment["id"],
                post_id=comment["post"],
                parent_id=comment["parent"],
                content=render_content(comment["content"]["rendered"]),
                link=comment["link"],
                date=comment["date"],
                author=comment["author_name"]
            )
            for comment in comments
        ]

    async def get_post(self, post_id: int) -> "PostDownloadPage":
        """Get a post's download page data from `farsroid.com` by its ID.

        Parameters:
            post_id (`int`): The post ID to get.

        Returns:
            A :class:`PostDownloadPage` object containing data like the post's title, download links, etc.
        """
        post_soup = await self._sess.get_soup(f"/?p={post_id}")
        parser = PostParser(post_soup)
        return parser.post_obj()

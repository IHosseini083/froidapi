from typing import Any, ClassVar, Dict, Optional
from urllib.parse import urljoin

from bs4 import BeautifulSoup
from httpx import AsyncClient, Response

from .exceptions import (
    AccessDeniedError,
    BadRequestError,
    FRoidAPIError,
    NotFoundError
)


class Session:
    """An asynchronous session for requesting `farsroid.com` endpoints.

    Parameters:
        html_parser (`str`, optional): The HTML parser to use for parsing the HTML responses
        as :class:`BeautifulSoup` objects.

    :class:`Session` is a wrapper for :class:`httpx.AsyncClient` that can
    validate the request and response and return various types of data
    (`json`, `text` and :class:`BeautifulSoup` object).

    Default HTML parser for :class:`BeautifulSoup` is `lxml` but you can
    specify another parser by setting the `html_parser` argument in the constructor.
    """

    BASE_URL: ClassVar[str] = "https://www.farsroid.com/"
    """Base URL for the `farsroid.com` API."""
    DEFAULT_HTML_PARSER: ClassVar[str] = "lxml"
    """Default HTML parser for :class:`BeautifulSoup`."""
    REQ_HEADERS: ClassVar[Dict[str, str]] = {
        "Host": "www.farsroid.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0",
    }
    """Headers to be added to every request."""
    
    __slots__ = ("_sess", "_html_parser")

    def __init__(self, html_parser: Optional[str] = None) -> None:
        self._html_parser = html_parser or self.DEFAULT_HTML_PARSER
        if not isinstance(self._html_parser, str):
            raise TypeError("html_parser must be a string or None")
        self._sess = AsyncClient()
        self._sess.headers.update(self.REQ_HEADERS)

    def __enter__(self) -> "Session":
        return self

    async def __aenter__(self) -> "Session":
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.close()

    def _response_validator(self, response: Response, url: str) -> Response:
        """Validate the given response and return it if everything was ok."""
        if not url.startswith(self.BASE_URL):
            raise ValueError(f"Invalid URL: {url!r}")
        st_code = response.status_code
        if st_code not in (200, 301, 302, 304):
            if st_code == 400:
                raise BadRequestError(f"Bad request", st_code)
            elif st_code in (401, 403):
                raise AccessDeniedError(f"Access denied", st_code)
            elif st_code == 404:
                raise NotFoundError(f"Not found", st_code)
            else:
                raise FRoidAPIError(f"Unknown error", st_code)
        return response

    async def request(self, method: str, endpoint: str, **kwargs) -> Response:
        """Make a request to the given URL and return the response.

        Parameters:
            method (`str`): The HTTP method to use.
            endpoint (`str`): The URL endpoint to request.
            **kwargs: Additional keyword arguments to pass to :meth:`httpx.AsyncClient.request` method.

        Returns:
            :class:`httpx.Response`: The response object.
        """
        url = urljoin(self.BASE_URL, endpoint)
        resp = await self._sess.request(method, url, follow_redirects=True, **kwargs)
        return self._response_validator(resp, url)

    async def get_json(self, endpoint: str, **kwargs) -> Any:
        """Make a GET request to the given URL and return the response as JSON data.

        Parameters:
            endpoint (`str`): The URL endpoint to request.
            **kwargs: Additional keyword arguments to pass to :meth:`Session.request` method.

        Returns:
            `dict`: The JSON response.
        """
        resp = await self.request("GET", endpoint, **kwargs)
        return resp.json()

    async def get_text(self, endpoint: str, **kwargs) -> str:
        """Make a GET request to the given URL and return the response as text.

        Parameters:
            endpoint (`str`): The URL endpoint to request.
            **kwargs: Additional keyword arguments to pass to :meth:`Session.request` method.

        Returns:
            `str`: The text response.
        """
        resp = await self.request("GET", endpoint, **kwargs)
        return resp.text

    async def get_soup(self, endpoint: str, **kwargs) -> BeautifulSoup:
        """Make a GET request to the given URL and return the response as a :class:`BeautifulSoup` object.

        Parameters:
            endpoint (`str`): The URL endpoint to request.
            **kwargs: Additional keyword arguments to pass to :meth:`Session.request` method.

        Returns:
            :class:`BeautifulSoup`: The BeautifulSoup object.
        """
        resp = await self.request("GET", endpoint, **kwargs)
        return BeautifulSoup(resp.text, self._html_parser)

    async def close(self) -> None:
        """Close the session."""
        await self._sess.aclose()

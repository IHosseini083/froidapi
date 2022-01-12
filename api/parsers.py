import re
from abc import ABC, abstractmethod
from typing import Any, Dict, Iterator, List, Optional

from bs4 import BeautifulSoup

from .exceptions import NotFoundError
from .models import (
    DownloadData,
    LegacySearchItem,
    PostDownloadPage,
    PostMedia,
    RelatedPost
)
from .utils import by_pattern

METADATA_NAMES: List[str] = [
    "required_android_version",
    "version",
    "category",
    "mode",
]
"""A list of metadata names that may be present in the `meta` field of response."""


def _parse_post_meta_search(post: Any) -> Optional[Dict[str, Any]]:
    """Parse a post metadata from the search result."""
    info_tags = post.find_all(class_="inf-cnt")
    if not info_tags:
        return
    meta = {}
    for info_tag in info_tags:
        key = info_tag.find("span").text
        value = info_tag.text.replace(key, "").strip()
        if "اندروید" in key:
            key = "required_android_version"
        elif "نسخه" in key:
            key = "version"
        else:
            key = ""
        if key and value:
            meta[key] = value
    return meta


def _parse_post_search_result(post: Any) -> Dict[str, Any]:
    """Parse a post content from the search result."""
    bookmark_btn = post.find("a", class_="bookmark-btn")
    data = {
        "url": post.find("a", href=lambda href: href and "farsroid.com" in href).get("href"),
        "title": post.find("h2").text.replace("\n", ""),
        "thumbnail": post.find("img").get("data-src"),
        "description": post.find(class_="excerpt").get_text(strip=True, separator=" "),
        "meta": _parse_post_meta_search(post),
    }
    if bookmark_btn:
        if bookmark_btn.get("data-id"):
            post_id = by_pattern(r"\d+", bookmark_btn.get("data-id"))
            data["post_id"] = int(post_id) if post_id else None
    return data


class ParserError(Exception):
    """Base error class for all API :class:`bs4.BeautifulSoup` response parsers' error."""

    def __init__(self, message: str, *args) -> None:
        super().__init__(message, *args)


class BaseParser(ABC):
    """Base class for all parsers."""

    __slots__ = ("_soup",)

    def __init__(self, soup_obj: "BeautifulSoup") -> None:
        if not isinstance(soup_obj, BeautifulSoup):
            raise ParserError(
                "Parser must be initialized with a BeautifulSoup object "
                f"not {type(soup_obj)}"
            )
        self._soup = soup_obj

    @abstractmethod
    def parsed(self) -> Any:
        ...

    def __getitem__(self, key: str) -> Any:
        if not isinstance(key, str):
            raise TypeError(
                "Parser keys must be strings, not {}".format(type(key))
            )
        return getattr(self, key, None)

    def __setitem__(self, key: str, value: Any) -> None:
        if not isinstance(key, str):
            raise TypeError(
                "Parser keys must be strings, not {}".format(type(key))
            )
        setattr(self, key, value)

    def __iter__(self) -> Iterator[Any]:
        """Iterate over the parsed data."""
        yield from self.parsed().items()

    def __next__(self) -> Any:
        """Return the next item in the parsed data."""
        return next(iter(self))

    def __contains__(self, key: str) -> bool:
        return self[key] is not None

    @property
    def soup(self) -> "BeautifulSoup":
        """Return the :class:`bs4.BeautifulSoup` object used to parse the data."""
        return self._soup


class LegacySearchParser(BaseParser):
    """A parser for searches that were made with `legacy` mode.

    Parameters:
        search_soup (:class:`bs4.BeautifulSoup`): The :class:`bs4.BeautifulSoup` 
        object return by :class:`~handler.APIHandler` class from web response.
    """

    def __init__(self, search_soup: "BeautifulSoup") -> None:
        super().__init__(search_soup)

    @property
    def total_pages(self) -> int:
        """Total number of pages available in search result."""
        page_numbers = self._soup.find_all(class_="page-numbers")
        if page_numbers and len(page_numbers) > 1:
            last_page = by_pattern(r"\d+", page_numbers[-1].text.replace(",", ""))
            return int(last_page) if last_page else 1
        return 1

    def iter_posts(self) -> Optional[Iterator[Dict[str, Any]]]:
        """Iterate over the posts found in the search result."""
        posts = self._soup.find_all(class_="post-item-wide")
        if not posts:
            return
        for post in posts:
            yield _parse_post_search_result(post)

    def parsed(self) -> List[LegacySearchItem]:
        """Return a list of :class:`~api.models.LegacySearchItem` objects from the search result."""
        return [LegacySearchItem(**post) for post in self.iter_posts()]


class PostParser(BaseParser):
    """Parse a post's download page data from its :class:`bs4.BeautifulSoup` object.

    Parameters:
        app_soup (:class:`bs4.BeautifulSoup`): The :class:`bs4.BeautifulSoup` 
        object of the post retrieved from the API.
    """

    __slots__ = ("_main_content", "_sidebar")

    def __init__(self, app_soup: "BeautifulSoup") -> None:
        super().__init__(app_soup)
        # main_content is the 'article' tag containing the main post content.
        self._main_content = self._soup.find(
            "article",
            # id must be starting with 'post-' and followed by a number.
            {"id": re.compile(r"^post-\d+$")}
        )
        if not self._main_content:
            raise NotFoundError("post not found", 404)
        self._sidebar = self._soup.find("aside", class_="sidebar-single")

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.post_id!r})"

    @property
    def post_id(self) -> int:
        """Return the post ID."""
        return int(self._main_content.get("id").split("-")[1])

    @property
    def title(self) -> str:
        """Return the title of the post."""
        return self._soup.title.text.strip()

    @property
    def description(self) -> str:
        """Return the description of the post."""
        post_content = self._main_content.find("div", class_="post-content")
        if not post_content:
            return ""
        return post_content.get_text(strip=True, separator=" ")

    @property
    def media(self) -> List[PostMedia]:
        """Return the media (image, video, etc.) of the post."""
        # screenshots gallery (contains screenshots and videos)
        ss_gallery = self._soup.find("section", class_="screenshots-gallery")
        if not ss_gallery:
            return []
        # TODO: write a better regex for media detection.
        media = ss_gallery.find_all(href=re.compile(r"\.jpg|\.png|\.mp4|\.webm"))
        if not media:
            return []
        # TODO: isolate the media type (image, video, etc.) in a separate file among the other constants.
        screenshots = [
            a.get("href") for a in media if a.get("href").endswith((".jpg", ".png"))
        ]
        videos = [a.get("href") for a in media if a.get("href").endswith((".mp4", ".webm"))]
        thumbnail = self._sidebar.find(class_="post-thumbnail").find("img").get("data-src")
        return [
            *[PostMedia(url=screenshot, media_type="screenshot")
              for screenshot in screenshots],
            *[PostMedia(url=video, media_type="video") for video in videos],
            PostMedia(url=thumbnail, media_type="thumbnail")
        ]

    @property
    def post_url(self) -> str:
        """URL of the post on the `farsroid.com` website."""
        return f"https://www.farsroid.com/?p={self.post_id}"

    @property
    def meta(self) -> Optional[Dict[str, str]]:
        """Return the post metadata."""
        # TODO: clean code 'version' detection.
        meta_data = {
            "version": by_pattern(r"\d+(\.\d+)*", self._main_content.find("h1").text),
        }
        # if the post belongs to a game, add the 'mode' to the metadata
        if game_mode := self._sidebar.find(class_="game-mode"):
            meta_data["mode"] = "offline" if "آفلاین" in game_mode.text else "online"
        meta_divs = self._sidebar.find_all("div", class_="inf-cnt")
        for meta_div in meta_divs:
            key: str = meta_div.span.text
            value: str = meta_div.text.replace(key, "").strip()
            # Change persian key to english key.
            if "اندروید" in key:
                key = "required_android_version"
            elif "دسته بندی" in key:
                key = "category"
            else:
                key = ""
            if key and value:
                meta_data[key] = value
        return meta_data

    @property
    def related_posts(self) -> Optional[List[RelatedPost]]:
        # "rps" stands for 'related posts section'
        rps = self._soup.find("section", class_="related-posts")
        if not rps:
            return
        # articles that has a class with pattern "post-\d+"
        related_articles = rps.find_all(class_=re.compile(r"^post-\d+"))
        if not related_articles:
            return
        # TODO: return a list of RelatedPost objects
        related_posts = []
        for article in related_articles:
            post_id = int(by_pattern(r"\d+", " ".join(article.get("class"))))
            post_title = article.get_text(strip=True, separator=" ")
            post_url = f"https://www.farsroid.com/?p={post_id}"
            post_thumbnail = article.find_all("img")[0].get("data-src")
            related_posts.append(
                RelatedPost(
                    post_id=post_id,
                    title=post_title,
                    url=post_url,
                    thumbnail=post_thumbnail
                )
            )
        return related_posts

    @property
    def gplay_url(self) -> Optional[str]:
        """Return the Google Play URL of the post if it exists."""
        gplay_url = self._soup.find(class_="gply-link")
        if not gplay_url:
            return
        return gplay_url.get("data-link", "")

    @property
    def download_data(self) -> Optional[List[DownloadData]]:
        """Return a list of :class:`DownloadData` objects (if there is any link) `None` otherwise."""
        download_box = self._soup.find(class_="download-links")
        if not download_box:
            return
        # download links must have one of the (".apk", ".zip", ".obb", ".rar") extensions
        dl_links = download_box.find_all(href=re.compile(r"\.(apk|zip|obb|rar)$"))
        if not dl_links:
            return
        return [
            DownloadData(url=a.get("href"), title=a.text.strip())
            for a in dl_links
        ]

    def post_obj(self) -> PostDownloadPage:
        """Return the :class:`Post` object for the post."""
        return PostDownloadPage(
            post_id=self.post_id,
            title=self.title,
            description=self.description,
            media=self.media,
            post_url=self.post_url,
            meta=self.meta,
            related_posts=self.related_posts,
            gplay_url=self.gplay_url,
            download_data=self.download_data
        )

    def parsed(self) -> Dict[str, Any]:
        """Return the parsed post data."""
        return self.post_obj().dict()

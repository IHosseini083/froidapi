import re
from abc import ABC, abstractmethod
from json import dumps as json_dumps
from typing import TYPE_CHECKING, Any, Dict, List, Optional

from .models import DownloadData, PostDownloadPgae, PostMedia, RelatedPost
from .utils import by_pattern

if TYPE_CHECKING:
    from bs4 import BeautifulSoup


class ParserError(Exception):
    """Base error class for all parser errors."""

    def __init__(self, message: str, *args) -> None:
        super().__init__(message, *args)


class Parser(ABC):
    def json(self) -> str:
        """Return a JSON representation of the parsed data."""
        return json_dumps(self.parsed())

    @abstractmethod
    def parsed(self) -> Dict[str, Any]:
        ...

    @property
    @abstractmethod
    def soup(self) -> "BeautifulSoup":
        ...


class PostParser(Parser):
    """Parse a post data from its :class:`bs4.BeautifulSoup` object.

    Parameters:
        app_soup (:class:`bs4.BeautifulSoup`): The :class:`bs4.BeautifulSoup` 
        object of the post retrieved from the API.
    """

    __slots__ = ("_soup", "_main_content", "_sidebar")

    def __init__(self, app_soup: "BeautifulSoup") -> None:
        self._soup = app_soup
        # main_content is the 'article' tag containing the main post content.
        self._main_content = self._soup.find(
            "article",
            # id must be statring with 'post-' and followed by a number.
            {"id": re.compile(r"^post-\d+$")}
        )
        if not self._main_content:
            raise ParserError("Could not find main content")
        self._sidebar = self._soup.find("aside", class_="sidebar-single")

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.post_id!r})"

    @property
    def soup(self) -> "BeautifulSoup":
        """Return the :class:`bs4.BeautifulSoup` object of the post."""
        return self._soup

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
        screenshots = [
            a.get("href") for a in media if a.get("href").endswith((".jpg", ".png"))
        ]
        videos = [a.get("href") for a in media if a.get("href").endswith((".mp4", ".webm"))]
        thubmnail = self._sidebar.find(class_="post-thumbnail").find("img").get("data-src")
        return [
            *[PostMedia(url=screenshot, media_type="screenshot") for screenshot in screenshots],
            *[PostMedia(url=video, media_type="video") for video in videos],
            PostMedia(url=thubmnail, media_type="thumbnail")
        ]

    @property
    def post_url(self) -> str:
        """URL of the post on the `farsroid.com` website."""
        return f"https://www.farsroid.com/?p={self.post_id}"
    
    @property
    def meta(self) -> Optional[Dict[str, str]]:
        """Return the post meta data."""
        # TODO: clean code 'version' detection.
        meta_data = {
            "version": by_pattern(r"\d+(\.\d+)*", self._main_content.find("h1").text),
        }
        # if the post belongs to a game, add the 'mode' to the meta data
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
                key = None
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

    def post_obj(self) -> PostDownloadPgae:
        """Return the :class:`Post` object for the post."""
        return PostDownloadPgae(
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

import re
from typing import Iterable, Optional, Union

from bs4 import BeautifulSoup


def render_content(content: str) -> str:
    """Renders content from HTML to plain text."""
    if not content:
        return ""
    soup = BeautifulSoup(content, "lxml")
    return soup.get_text(separator=" ", strip=True)


def by_pattern(pattern: str, text: Union[str, Iterable[str]]) -> Optional[Union[str, Iterable[str]]]:
    """Finds a match by a pattern in a string or an iterable of strings."""
    if isinstance(text, str):
        match = re.search(pattern, text)
        if match:
            return match.group()
    elif isinstance(text, Iterable):
        return [match.group() for match in re.finditer(pattern, text) if match]
    return
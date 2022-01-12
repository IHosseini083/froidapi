import re
from typing import Iterable, Optional, Union

from bs4 import BeautifulSoup


def render_content(content: str) -> str:
    """Renders content from HTML to plain text."""
    if not content:
        return ""
    soup = BeautifulSoup(content, "lxml")
    return soup.get_text(separator=" ", strip=True)


def by_pattern(pattern: str, text: str) -> Optional[str]:
    """Returns the first match of the given pattern in the given text."""
    pattern_re = re.compile(pattern)
    if pattern_re.search(text):
        return pattern_re.search(text).group()
    return

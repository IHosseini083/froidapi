from bs4 import BeautifulSoup


def render_content(content: str) -> str:
    """Renders content from HTML to plain text."""
    if not content:
        return ""
    soup = BeautifulSoup(content, "lxml")
    return soup.get_text(separator=" ", strip=True)

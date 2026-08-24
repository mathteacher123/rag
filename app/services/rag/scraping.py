import trafilatura
from bs4 import BeautifulSoup


def fetch_html(url: str) -> tuple[str | None, str]:
    """Fetch content from a URL and return (title, raw HTML).

    Args:
        url: The URL to fetch.

    Returns:
        Tuple of (title, body HTML). title is None if not found.
    """
    downloaded = trafilatura.fetch_url(url)
    if downloaded is None:
        return None, ""

    soup = BeautifulSoup(downloaded, "html.parser")
    title_tag = soup.find("title")
    title = title_tag.get_text(" ", strip=True) if title_tag else None

    html_content = trafilatura.extract(
        downloaded, include_links=True, include_images=True, output_format="html", favor_recall=True
    )
    if html_content is None:
        return title, ""
    return title, html_content

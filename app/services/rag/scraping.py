import trafilatura
from markdownify import markdownify as md


def fetch_and_convert_to_markdown(url: str) -> str:
    """Fetch content from a URL and convert it to markdown.

    Args:
        url: The URL to fetch and convert.

    Returns:
        The converted markdown content.
    """
    downloaded = trafilatura.fetch_url(url)
    if downloaded is None:
        return ""
    html_content = trafilatura.extract(
        downloaded, include_links=True, include_images=True, output_format="html"
    )
    if html_content is None:
        return ""
    return md(html_content)

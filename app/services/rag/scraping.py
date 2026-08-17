import trafilatura


def fetch_html(url: str) -> str:
    """Fetch content from a URL and return raw HTML.

    Args:
        url: The URL to fetch and convert.

    Returns:
        The raw HTML content, or empty string on failure.
    """
    downloaded = trafilatura.fetch_url(url)
    if downloaded is None:
        return ""
    html_content = trafilatura.extract(
        downloaded, include_links=True, include_images=True, output_format="html"
    )
    if html_content is None:
        return ""
    return html_content

import trafilatura
from bs4 import BeautifulSoup


def fetch_url(url: str) -> dict:
    """
    Fetches a URL, extracts markdown content, and secures metadata
    (title, canonical url). Provides a bulletproof BeautifulSoup
    fallback for missing titles.
    """
    # 1. Fetch the raw HTML string
    downloaded = trafilatura.fetch_url(url)
    if not downloaded:
        return {"text": "", "metadata": {"title": None, "canonical_url": url}}

    # 2. Extract Metadata via Trafilatura
    meta = trafilatura.extract_metadata(downloaded)
    title = meta.title if meta else None
    canonical_url = meta.url if (meta and meta.url) else None

    # 3. Fallback to BeautifulSoup if title is blank/None
    if not title or not title.strip():
        soup = BeautifulSoup(downloaded, "html.parser")
        title_tag = soup.find("title")
        title = title_tag.get_text(" ", strip=True) if title_tag else None

    # 4. Extract Main Content to Markdown using your specific flags
    markdown_content = trafilatura.extract(
        downloaded,
        output_format="markdown",
        include_comments=False,
        include_formatting=True,
        favor_precision=True,
    )

    return {
        "text": markdown_content or "",
        "metadata": {"title": title, "canonical_url": canonical_url},
    }

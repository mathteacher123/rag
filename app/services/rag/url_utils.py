from urllib.parse import urlparse, urlunparse


def normalize_url(url: str) -> str:
    parsed = urlparse(url)
    return urlunparse(
        (
            "https",
            parsed.netloc.lower(),
            parsed.path.rstrip("/") or "/",
            parsed.params,
            "",
            "",
        )
    )

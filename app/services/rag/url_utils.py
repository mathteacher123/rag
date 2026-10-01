import hashlib
from urllib.parse import parse_qsl, urlencode, urljoin, urlsplit, urlunsplit

TRACKING_PARAMS = {
    "fbclid",
    "gclid",
    "msclkid",
    "dclid",
    "ref",
    "session",
    "sessionid",
    "mc_cid",
    "mc_eid",
    "igshid",
}
TRACKING_PREFIXES = ("utm_",)


def normalize_url(url: str) -> str:
    parts = urlsplit(url.strip())
    host = (parts.hostname or "").lower()

    # keep only non-default ports (default = 80 for http, 443 for https)
    port = parts.port
    if port and port not in (80, 443):
        host = f"{host}:{port}"

    # trailing slash off, except for the root path
    path = parts.path.rstrip("/") or "/"

    # drop tracking params, keep the rest, sort for stable order
    query = sorted(
        (k, v)
        for k, v in parse_qsl(parts.query, keep_blank_values=True)
        if k.lower() not in TRACKING_PARAMS
        and not k.lower().startswith(TRACKING_PREFIXES)
    )

    # force https, drop fragment
    return urlunsplit(("https", host, path, urlencode(query), ""))


def make_doc_id(url: str, canonical_url: str | None = None) -> str:
    # canonical may be relative (e.g. "/page"), so resolve it against the fetched url
    source = urljoin(url, canonical_url) if canonical_url else url
    return hashlib.sha256(normalize_url(source).encode("utf-8")).hexdigest()

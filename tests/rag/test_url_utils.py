from app.services.rag.url_utils import normalize_url


def test_strips_query_string():
    assert (
        normalize_url("https://example.com/page?ref=home") == "https://example.com/page"
    )


def test_strips_fragment():
    assert (
        normalize_url("https://example.com/page#section1") == "https://example.com/page"
    )


def test_strips_trailing_slash():
    assert normalize_url("https://example.com/page/") == "https://example.com/page"


def test_keeps_root_slash():
    assert normalize_url("https://example.com/") == "https://example.com/"


def test_lowercases_domain():
    assert normalize_url("https://EXAMPLE.COM/Page") == "https://example.com/Page"


def test_forces_https():
    assert normalize_url("http://example.com/page") == "https://example.com/page"


def test_strips_both_query_and_fragment():
    assert (
        normalize_url("https://example.com/page?x=1#top") == "https://example.com/page"
    )

from wiki_scraper.wiki_page.utils import extract_id_and_title


def test_extracts_id_and_title_correctly():
    html = """
    <script>
        "wgArticleId" : 12345,
        "wgPageName" :    "Bee",
    </script>
    """
    result = extract_id_and_title(html)
    assert result == (12345, "Bee")


def test_missing_id_returns_none():
    html = '<script>"wgPageName" : "Bee";</script>'
    result = extract_id_and_title(html)
    assert result is None


def test_missing_name_returns_none():
    html = '<script>var "wgArticleId" : 12345;</script>'
    result = extract_id_and_title(html)
    assert result is None


def test_malformed_html_returns_none():
    html = '<div>Random stuff, no "wgPageName" here</div>'
    result = extract_id_and_title(html)
    assert result is None


def test_canonical_title_used_if_page_name_missing():
    html = """
    <script>
        "wgArticleId" : 67890,
        "wgCanonicalTitle" : "Creeper";
    </script>
    """
    result = extract_id_and_title(html)
    assert result == (67890, "Creeper")

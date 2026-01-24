from collections import Counter

from bs4 import BeautifulSoup, Tag

from wiki_scraper.wiki_page.utils import extract_word_counts


def make_tag(html: str) -> Tag:
    """Helper to create a bs4 Tag from HTML string."""
    soup = BeautifulSoup(html, "html.parser")
    return soup


def test_basic_word_count():
    html = "<p>Foo bar foo baz</p>"
    tag = make_tag(html)
    counts = extract_word_counts(tag)
    assert counts == Counter({"foo": 2, "bar": 1, "baz": 1})


def test_empty_content():
    html = "<p></p>"
    tag = make_tag(html)
    counts = extract_word_counts(tag)
    assert counts == Counter()


def test_unicode_words():
    html = "<p>naïve café résumé coöperate</p>"
    tag = make_tag(html)
    counts = extract_word_counts(tag)
    expected = Counter({"naïve": 1, "café": 1, "résumé": 1, "coöperate": 1})
    assert counts == expected


def test_hyphens_and_apostrophes():
    html = "<p>mother-in-law it's high-quality O'Hare</p>"
    tag = make_tag(html)
    counts = extract_word_counts(tag)
    expected = Counter(
        {"mother-in-law": 1, "it's": 1, "high-quality": 1, "o'hare": 1}
    )
    assert counts == expected


def test_ignores_numbers_and_symbols():
    html = "<p>foo123 ,bar! 42baz under_score</p>"
    tag = make_tag(html)
    counts = extract_word_counts(tag)
    expected = Counter({"bar": 1})
    assert counts == expected

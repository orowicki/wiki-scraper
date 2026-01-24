from bs4 import BeautifulSoup

from wiki_scraper.wiki_page.utils import extract_paragraphs


def make_tag(html: str):
    """Helper to create a bs4 Tag from HTML string."""
    soup = BeautifulSoup(html, "html.parser")
    return soup


def test_basic_paragraph_extraction():
    html = "<div><p>First paragraph.</p><p>Second paragraph.</p></div>"
    tag = make_tag(html)
    paragraphs = extract_paragraphs(tag)
    assert paragraphs == ["First paragraph.", "Second paragraph."]


def test_paragraphs_text_is_clean():
    html = """
    <div>
        <p>Main <a href='/wiki/Foo'>Foo</a> paragraph w/ <b>bold</b> text.</p>
        <p><i>Italic</i> paragraph.</p>
    </div>
    """
    tag = make_tag(html)
    paragraphs = extract_paragraphs(tag)

    assert paragraphs == [
        "Main Foo paragraph w/ bold text.",
        "Italic paragraph.",
    ]


def test_skips_table_and_aside_paragraphs():
    html = """
    <div>
        <p>Main paragraph.</p>
        <table><p>Table paragraph.</p></table>
        <aside><p>Aside paragraph.</p></aside>
    </div>
    """
    tag = make_tag(html)
    paragraphs = extract_paragraphs(tag)
    assert paragraphs == ["Main paragraph."]


def test_skips_infobox_and_thumb():
    html = """
    <div>
        <p>Main paragraph.</p>
        <div class="infobox"><p>Infobox paragraph.</p></div>
        <div class="thumb"><p>Thumb paragraph.</p></div>
    </div>
    """
    tag = make_tag(html)
    paragraphs = extract_paragraphs(tag)
    assert paragraphs == ["Main paragraph."]


def test_empty_paragraphs_ignored():
    html = "<div><p> </p><p>Main paragraph.</p></div>"
    tag = make_tag(html)
    paragraphs = extract_paragraphs(tag)
    assert paragraphs == ["Main paragraph."]


def test_multiple_skips_combined():
    html = """
    <div>
        <p>Main paragraph.</p>
        <aside><p>Aside paragraph.</p></aside>
        <table><p>Table paragraph.</p></table>
        <figure><p>Figure paragraph.</p></figure>
        <div class="navbox"><p>Navbox paragraph.</p></div>
        <div class="toc"><p>TOC paragraph.</p></div>
    </div>
    """
    tag = make_tag(html)
    paragraphs = extract_paragraphs(tag)
    assert paragraphs == ["Main paragraph."]

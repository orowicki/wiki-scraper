"""
Paragraph extraction utility for Wiki articles.

Provides a function to extract the main paragraphs from a Wiki article
content, skipping tables, sidebars, notes, and other non-main text.
"""

from bs4 import Tag

SKIP_SELECTOR = (
    "table p, aside p, figure p, .infobox p, .thumb p, "
    ".sidebar p, .navbox p, .toc p, .hatnote p"
)


def extract_paragraphs(content: Tag) -> list[str]:
    """
    Extract the main paragraphs from a Wiki article content Tag.

    This function filters out paragraphs that are inside tables,
    sidebars, figure captions, infoboxes, navigation boxes,
    table of contents, or hatnotes.

    Parameters
    ----------
    content : Tag
        A bs4 Tag containing the main content of a Wiki article.

    Returns
    -------
    list[str]
        A list of strings containing the filtered paragraphs.
    """
    paragraphs = content.find_all("p")

    skipped = set(content.select(SKIP_SELECTOR))
    paragraphs = [
        p.get_text().strip()
        for p in paragraphs
        if p not in skipped and p.get_text(" ", strip=True)
    ]

    return paragraphs

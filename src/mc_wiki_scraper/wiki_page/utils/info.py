"""
Info extraction utility for Wiki articles

Provides a function to extract article ID and page name the HTML of a
Wiki article.
"""

import re

PAGE_ID_RE = re.compile(r'"wgArticleId"\s*:\s*(\d+)')
PAGE_NAME_RE = re.compile(r'"wg(PageName|CanonicalTitle)"\s*:\s*"([^"]+)"')


def extract_id_and_title(html: str) -> tuple[int, str] | None:
    """
    Extract the article ID and page name from a Wiki article HTML
    string.

    Parameters
    ----------
    html : str
        The HTML content of a Wiki article page.

    Returns
    -------
    tuple[int, str] | None
        A tuple containing the article ID and the page name, or
        None if either could not be found.
    """
    id_match = PAGE_ID_RE.search(html)
    name_match = PAGE_NAME_RE.search(html)

    if not id_match or not name_match:
        return None

    page_id = int(id_match.group(1))
    page_name = name_match.group(2)

    return page_id, page_name

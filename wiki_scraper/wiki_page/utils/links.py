"""
Internal link extraction utility for Wiki articles.

Provides a function to extract normalized internal link phrases from
a bs4 Tag containing article content, ignoring external links,
query parameters, and blocked namespaces.
"""

from bs4 import Tag

WIKI_PREFIX = "/w/"
BLOCKED_PREFIXES = (
    "File:",
    "Category:",
    "Special:",
    "Help:",
    "Talk:",
    "Template:",
    "User:",
    "User_talk:",
)


def normalize_phrase_from_href(href: str) -> str | None:
    """
    Normalize a Wikipedia href to a phrase.

    Parameters
    ----------
    href : str
        The href attribute of an <a> tag.

    Returns
    -------
    str | None
        The normalized phrase if valid, or None if the link is external,
        points to a blocked namespace, or contains query parameters.
    """
    if not href.startswith(WIKI_PREFIX) or "?" in href:
        return None

    href = href.split("#", 1)[0]
    phrase = href[len(WIKI_PREFIX) :]

    if phrase.startswith(BLOCKED_PREFIXES):
        return None

    return phrase


def extract_internal_link_phrases(content: Tag) -> set[str]:
    """
    Extract all normalized internal link phrases from
    a Wiki article's content.

    Parameters
    ----------
    content : Tag
        A bs4 Tag containing the main content of a Wiki article.

    Returns
    -------
    set[str]
        A set of normalized internal link phrases, ignoring external
        links, query parameters, and blocked namespaces.
    """
    phrases = set()

    for a in content.select("a[href]"):
        href = a["href"]

        if isinstance(href, list):
            href = "".join(href)

        phrase = normalize_phrase_from_href(href)
        if phrase is not None:
            phrases.add(phrase)

    return phrases

"""
utils
-----
The ``utils`` package provides a variety of utilities for fetching Wiki
articles and extracting their contents.

Functionality:
- start a ``requests`` session and fetch HTML from a link
- extract article ID and its canonical title
- extract an article's paragraphs
- extract phrases from internal links from within an article
- extract tables from an article
- extract word counts from an article
"""

from .fetch import fetch_html, get_session
from .info import extract_id_and_title
from .links import extract_internal_link_phrases, normalize_phrase_from_href
from .paragraphs import extract_paragraphs
from .tables import extract_tables
from .word_counts import extract_word_counts

__all__ = [
    "fetch_html",
    "get_session",
    "extract_id_and_title",
    "extract_paragraphs",
    "normalize_phrase_from_href",
    "extract_internal_link_phrases",
    "extract_tables",
    "extract_word_counts",
]

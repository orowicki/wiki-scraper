"""
Word count extraction utility for Wiki articles.

Provides a function to extract word counts from a bs4 Tag and
convert them into a Counter.
"""

from collections import Counter
import regex
from bs4 import Tag


def extract_word_counts(content: Tag) -> Counter:
    """
    Extract words from a Tag into a Counter.

    Words are normalized to lowercase. Only words composed entirely
    of letters (Unicode letters allowed), with optional internal
    hyphens or apostrophes, are counted. Words containing digits
    or other symbols are ignored.

    Parameters
    ----------
    content : Tag
        bs4 Tag containing the content to process

    Returns
    -------
    Counter
        a Counter mapping each word to its frequency in the content
    """

    text = content.get_text(separator=" ", strip=True).lower()
    words = regex.findall(r"\b\p{L}+(?:[-']\p{L}+)*\b", text)

    return Counter(words)

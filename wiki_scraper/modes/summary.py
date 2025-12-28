"""
summary.py
----------
Provides functions to find and print a summary of a chosen article.

Functions:
- get_summary: returns a string containing the summary
- summarize: prints out the summary
"""

from bs4 import BeautifulSoup
import re


def get_summary(soup: BeautifulSoup) -> str:
    """
    Finds and formats the first paragraph of the article given
    by `soup`.

    Returns the resulting string.
    """

    content = soup.select_one("#mw-content-text .mw-parser-output")
    if not content:
        raise ValueError("No content found")

    for p in content.find_all("p"):
        text = p.get_text(" ", strip=True)

        if not text:
            continue

        if p.find_parent(["table", "aside"]):
            continue

        text = re.sub(r"\s+([.,!?;:])", r"\1", text)
        return text

    raise ValueError("No paragraph found")


def summarize(soup: BeautifulSoup) -> None:
    """Prints out the summary of the article given by `soup`."""

    summary = get_summary(soup)
    print(summary)

"""
summary.py
----------
Provides functions to find and print a summary of a chosen article.

Functions:
- get_summary: returns a string containing the summary
- summarize: prints out the summary
"""

from bs4 import Tag


def get_valid_parapraphs(content: Tag) -> list[Tag]:
    skip_selector = (
        "table p, aside p, figure p, .infobox p, .thumb p, "
        ".sidebar p, .navbox p, .toc p, .hatnote p"
    )

    candidates = content.find_all("p")

    skipped = set(content.select(skip_selector))
    candidates = [p for p in candidates if p not in skipped]

    return candidates


def get_summary(content: Tag) -> str:
    """
    Return the first paragraph from an article body.
    """

    candidates = get_valid_parapraphs(content)

    for p in candidates:
        if not p.get_text(" ", strip=True):
            continue

        return p.get_text().strip()

    raise ValueError("No paragraph found")


def run_summary_mode(content: Tag) -> None:
    """Prints out the summary of the article given by `soup`."""

    summary = get_summary(content)
    print(summary)

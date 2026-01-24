"""
Count words mode for Wiki articles.

Provides the ``CountWordsMode`` class, which extracts word counts
from a Wiki article and updates a JSON file with aggregated results.
"""

import json
from collections import Counter
from pathlib import Path

from ..wiki_page import WikiPage


class CountWordsMode:
    """
    Read word counts from a Wiki article and update a JSON file.

    Parameters
    ----------
    page : WikiPage
        A WikiPage instance representing the article
    """

    JSONPATH = "word-counts.json"

    def __init__(self, page: WikiPage):
        self.page = page

    def run(self) -> None:
        """
        Update a JSON file with word counts from the article.

        If the article has no content, an informative message is printed
        instead.
        """
        counts = self.page.get_word_counts()
        if counts is None:
            print(f"No word counts available for {self.page.phrase}")
            return

        self._update_json(counts)

    def _update_json(self, counts: Counter) -> None:
        path = Path(self.JSONPATH)

        try:
            with open(path, encoding="utf-8") as f:
                total_counts = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            total_counts = {}

        for word, c in counts.items():
            total_counts[word] = total_counts.get(word, 0) + c

        with open(path, "w", encoding="utf-8") as f:
            json.dump(total_counts, f, ensure_ascii=False, indent=2)

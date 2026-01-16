"""
summary.py
----------
Provides functions to find and print a summary of a chosen article.

Functions:
- get_summary: returns a string containing the summary
- summarize: prints out the summary
"""

from page_fetcher import WikiPage

class SummaryMode:
    def __init__(self, page: WikiPage):
        self.page = page

    def run(self) -> None:
        paragraphs = self.page.get_paragraphs()
        if paragraphs is None:
            print(f"No valid paragraphs in {self.page.phrase}")
            return

        first_paragraph = paragraphs[0].get_text().strip()
        print(first_paragraph)

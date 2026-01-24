"""
Summary mode for Wiki articles.

Provides the ``SummaryMode`` class, which prints the first
paragraph (summary) of a Wiki article.
"""

from ..wiki_page import WikiPage


class SummaryMode:
    """
    Print the summary paragraph of a Wiki article.

    Parameters
    ----------
    page : WikiPage
        A WikiPage instance representing the article to summarize.
    """

    def __init__(self, page: WikiPage):
        self.page = page

    def run(self) -> None:
        """
        Print the first paragraph of the article.

        If the article has no valid paragraphs, an informative message
        is printed instead.
        """
        paragraphs = self.page.get_paragraphs()
        if not paragraphs:
            print(f"No paragraphs for {self.page.phrase}")
            return

        print(paragraphs[0])

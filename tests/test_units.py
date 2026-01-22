import unittest
from collections import Counter
from bs4 import BeautifulSoup

from wiki_scraper.wiki_page.utils.info import extract_id_and_title
from wiki_scraper.wiki_page.utils.paragraphs import extract_paragraphs
from wiki_scraper.wiki_page.utils.links import normalize_phrase_from_href
from wiki_scraper.wiki_page.utils.word_counts import extract_word_counts


class TestWikiHelpers(unittest.TestCase):
    def test_extract_id_and_title(self):
        html = (
            '<script>var wgArticleId=123; var wgPageName="Test_Page";</script>'
        )
        result = extract_id_and_title(html)
        self.assertEqual(result, (123, "Test_Page"))

    def test_extract_paragraphs_filters_skipped(self):
        html = """
        <div id="mw-content-text">
            <p>Keep this paragraph.</p>
            <table><p>Skip this paragraph.</p></table>
        </div>
        """
        soup = BeautifulSoup(html, "html.parser")
        content = soup.select_one("#mw-content-text")
        assert content is not None
        paragraphs = extract_paragraphs(content)
        self.assertEqual(len(paragraphs), 1)
        self.assertEqual(
            paragraphs[0].get_text(strip=True), "Keep this paragraph."
        )

    def test_normalize_href(self):
        self.assertEqual(
            normalize_phrase_from_href("/w/Test_Page"), "Test_Page"
        )
        self.assertIsNone(normalize_phrase_from_href("/w/File:Example.png"))
        self.assertIsNone(normalize_phrase_from_href("/notwiki/Test_Page"))
        self.assertIsNone(normalize_phrase_from_href("/w/Test_Page#section"))
        self.assertIsNone(normalize_phrase_from_href("/w/Test_Page?query=1"))

    def test_extract_word_counts_only_letters(self):
        html = "<p>Hello world 123 !@# test</p>"
        soup = BeautifulSoup(html, "html.parser")
        tag = soup.p
        assert tag is not None
        counts = extract_word_counts(tag)
        expected = Counter({"hello": 1, "world": 1, "test": 1})
        self.assertEqual(counts, expected)


if __name__ == "__main__":
    unittest.main()

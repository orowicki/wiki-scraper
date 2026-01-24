import json
from collections import Counter
from pathlib import Path

from wiki_scraper.modes import CountWordsMode
from wiki_scraper.wiki_page import WikiPage

HERE = Path(__file__).parent


def test_count_words_integration(tmp_path):
    html_path = HERE.parent / "test_files" / "Creeper.html"
    page = WikiPage(html_file=html_path)
    mode = CountWordsMode(page)

    temp_json = tmp_path / "word-counts.json"
    mode.JSONPATH = temp_json

    mode.run()

    with open(temp_json, encoding="utf-8") as f:
        counts = json.load(f)

    counts = Counter(counts)

    expected_words = {
        "charged": 42,
        "explosion": 37,
        "hisses": 3,
        "proximity": 1,
    }

    for word, count in expected_words.items():
        assert counts[word] == count

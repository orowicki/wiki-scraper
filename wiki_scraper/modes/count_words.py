from collections import Counter
import json
from pathlib import Path
from wiki_page.wiki_page import WikiPage


class CountWordsMode:
    JSONPATH = "word-counts.json"

    def __init__(self, page: WikiPage):
        self.page = page

    def run(self):
        counts = self.page.get_word_counts()
        if counts is None:
            print(f"There is no article for {self.page.phrase}")
            return None

        self._update_json(counts)

    def _update_json(self, counts: Counter) -> None:
        path = Path(self.JSONPATH)

        if path.exists():
            with open(path) as f:
                total_counts = json.load(f)
        else:
            total_counts = {}

        for word, c in counts.items():
            total_counts[word] = total_counts.get(word, 0) + c

        with open(path, "w", encoding="utf-8") as f:
            json.dump(total_counts, f, ensure_ascii=False, indent=2)

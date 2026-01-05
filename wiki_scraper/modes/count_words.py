from bs4 import Tag
import re
from collections import Counter
import json
from pathlib import Path

JSONPATH = "word-counts.json"


def get_counts(content: Tag) -> Counter:
    text = content.get_text(separator=" ", strip=True).lower()

    words = re.findall(r"\w+", text)
    words = [w for w in words if not w.isdigit()]

    counts = Counter(words)

    return counts


def update_json(counts: Counter) -> None:
    path = Path(JSONPATH)

    if path.exists():
        with open(path) as f:
            total_counts = json.load(f)
    else:
        total_counts = {}

    for word, c in counts.items():
        total_counts[word] = total_counts.get(word, 0) + c

    with open(path, "w", encoding="utf-8") as f:
        json.dump(total_counts, f, ensure_ascii=False, indent=2)


def run_count_words_mode(content: Tag) -> None:
    counts = get_counts(content)
    update_json(counts)

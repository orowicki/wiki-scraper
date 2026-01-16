import re
from collections import Counter
from bs4 import Tag


def extract_word_counts(content: Tag) -> Counter:
    text = content.get_text(separator=" ", strip=True).lower()

    words = re.findall(r"\w+", text)
    words = [w for w in words if not w.isdigit()]

    counts = Counter(words)

    return counts

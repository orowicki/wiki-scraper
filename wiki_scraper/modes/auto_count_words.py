from bs4 import Tag
from modes.count_words import run_count_words
from page_fetcher import WikiPage
from collections import deque
import time
import re


WIKI_PREFIX = "/w/"
BLOCKED_PREFIXES = (
    "File:",
    "Category:",
    "Special:",
    "Help:",
    "Talk:",
)


def format_phrase(phrase: str) -> str:
    parts = re.split(r"[\s_]+", phrase.strip())
    parts = [p.capitalize() for p in parts if p]

    return "_".join(parts)


def normalize_phrase_from_href(href: str) -> str | None:
    if not href.startswith(WIKI_PREFIX):
        return None

    # drop search/edit/etc parameters
    if "?" in href:
        return None

    phrase = href[len(WIKI_PREFIX) :]

    if phrase.startswith(BLOCKED_PREFIXES):
        return None

    return phrase


def extract_link_phrases(content: Tag) -> set[str]:
    phrases = set()

    for a in content.select("a[href]"):

        href = a["href"]

        if isinstance(href, list):
            href = "".join(href)

        phrase = normalize_phrase_from_href(href)
        if phrase:
            phrases.add(phrase)

    return phrases


def run_auto_count_words(
    starter_phrase: str,
    max_depth: int,
    wait: float,
):
    starter_phrase = format_phrase(starter_phrase)
    queue = deque([(starter_phrase, 0)])
    visited = {starter_phrase}

    while queue:
        phrase, depth = queue.popleft()

        print(phrase)

        content = WikiPage(phrase).fetch_content()

        if depth < max_depth:
            for link_phrase in extract_link_phrases(content):
                if link_phrase not in visited:
                    visited.add(link_phrase)
                    queue.append((link_phrase, depth + 1))

        run_count_words(content)
        time.sleep(wait)

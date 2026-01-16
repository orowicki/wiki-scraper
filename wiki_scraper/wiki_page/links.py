from bs4 import Tag

WIKI_PREFIX = "/w/"
BLOCKED_PREFIXES = (
    "File:",
    "Category:",
    "Special:",
    "Help:",
    "Talk:",
    "Template:",
    "User:",
    "User_talk:",
)


def _normalize_phrase_from_href(href: str) -> str | None:
    if not href.startswith(WIKI_PREFIX) or "?" in href:
        return None

    href = href.split("#", 1)[0]
    phrase = href[len(WIKI_PREFIX) :]

    if phrase.startswith(BLOCKED_PREFIXES):
        return None

    return phrase


def extract_internal_link_phrases(content: Tag) -> set[str]:
    phrases = set()

    for a in content.select("a[href]"):
        href = a["href"]

        if isinstance(href, list):
            href = "".join(href)

        phrase = _normalize_phrase_from_href(href)
        if phrase is not None:
            phrases.add(phrase)

    return phrases

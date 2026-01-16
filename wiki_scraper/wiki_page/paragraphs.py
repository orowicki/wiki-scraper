from bs4 import Tag

SKIP_SELECTOR = (
    "table p, aside p, figure p, .infobox p, .thumb p, "
    ".sidebar p, .navbox p, .toc p, .hatnote p"
)


def extract_paragraphs(content: Tag) -> list[Tag]:
    paragraphs = content.find_all("p")

    skipped = set(content.select(SKIP_SELECTOR))
    paragraphs = [
        p
        for p in paragraphs
        if p not in skipped and p.get_text(" ", strip=True) is not None
    ]

    return paragraphs

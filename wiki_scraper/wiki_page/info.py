import re

PAGE_ID_RE = re.compile(r'"wgArticleId"\s*:\s*(\d+)')
PAGE_NAME_RE = re.compile(r'"wg(PageName|CanonicalTitle)"\s*:\s*"([^"]+)"')


def extract_id_and_title(html: str) -> tuple[int, str] | None:
    id_match = PAGE_ID_RE.search(html)
    name_match = PAGE_NAME_RE.search(html)

    if not id_match or not name_match:
        return None

    page_id = int(id_match.group(1))
    page_name = name_match.group(2)

    return page_id, page_name

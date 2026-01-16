import requests
from requests.exceptions import HTTPError

HEADERS = {
    "User-Agent": "wiki-scraper (for university project | "
    "contact: oskar.rowicki@gmail.com)"
}
TIMEOUT = 10

_session: requests.Session | None = None


def get_session() -> requests.Session:
    global _session
    if _session is None:
        s = requests.Session()
        s.headers.update(HEADERS)
        _session = s

    return _session


def close_session() -> None:
    global _session
    if _session is not None:
        _session.close()
        _session = None


def fetch_html(url: str) -> str | None:
    try:
        response = get_session().get(url, timeout=TIMEOUT)
        response.raise_for_status()
        return response.text

    except HTTPError as e:
        if e.response is not None and e.response.status_code == 404:
            return None
        else:
            raise

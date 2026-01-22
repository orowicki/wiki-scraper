"""
HTML fetching utilities for Wiki articles.

Provides a requests session with default headers and functions
to fetch HTML content safely, handling 404 errors gracefully.
"""

import requests
from requests.exceptions import HTTPError

HEADERS = {
    "User-Agent": "wiki-scraper (for university project | "
    "contact: oskar.rowicki@gmail.com)"
}
TIMEOUT = 10

_session: requests.Session | None = None


def get_session() -> requests.Session:
    """
    Get a singleton requests.Session configured with default headers.

    Returns
    -------
    requests.Session
        A persistent session object for making HTTP requests.
    """
    global _session
    if _session is None:
        s = requests.Session()
        s.headers.update(HEADERS)
        _session = s

    return _session


def fetch_html(url: str) -> str | None:
    """
    Fetch the HTML content of a URL using the global session.

    Parameters
    ----------
    url : str
        The URL of the page to fetch.

    Returns
    -------
    str | None
        The HTML content as a string, or None if the URL returns a 404.

    Raises
    ------
    HTTPError
        For HTTP errors other than 404.
    """
    try:
        response = get_session().get(url, timeout=TIMEOUT)
        response.raise_for_status()
        return response.text

    except HTTPError as e:
        if e.response is not None and e.response.status_code == 404:
            return None
        else:
            raise

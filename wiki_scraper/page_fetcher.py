import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from bs4 import Tag

BASE_URL = "https://minecraft.wiki/w/"
HEADERS = {
    "User-Agent": "wiki-scraper (for university project | "
    "contact: oskar.rowicki@gmail.com)"
}

session = requests.Session()
session.headers.update(HEADERS)


def normalize_phrase(phrase: str) -> str:
    return phrase.strip().replace(" ", "_")


def fetch_soup(phrase: str) -> BeautifulSoup:
    url = urljoin(BASE_URL, normalize_phrase(phrase))

    response = session.get(url, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    if soup.select_one(".noarticletext"):
        raise ValueError(f"Page '{phrase}' does not exist on minecraft.wiki")

    # disambiguation page case TODO

    return soup


def fetch_content(phrase: str) -> Tag:
    soup = fetch_soup(phrase)

    content = soup.select_one("#mw-content-text .mw-parser-output")
    if not content:
        raise ValueError("No content found")

    return content

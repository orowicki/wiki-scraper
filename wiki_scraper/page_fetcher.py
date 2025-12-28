import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup

BASE_URL = "https://minecraft.wiki/w/"
HEADERS = {
    "User-Agent": "wiki-scraper (for university project | "
    "contact: oskar.rowicki@gmail.com)"
}

session = requests.Session()
session.headers.update(HEADERS)


def normalize_phrase(phrase: str) -> str:
    return phrase.strip().replace(" ", "_")


def fetch_page(phrase: str) -> BeautifulSoup:
    url = urljoin(BASE_URL, normalize_phrase(phrase))

    response = session.get(url, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    if soup.select_one(".noarticletext"):
        raise ValueError(f"Page '{phrase}' does not exist on minecraft.wiki")

    return soup

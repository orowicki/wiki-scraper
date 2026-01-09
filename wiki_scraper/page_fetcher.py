import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from bs4 import Tag
from pathlib import Path

BASE_URL = "https://minecraft.wiki/w/"
HEADERS = {
    "User-Agent": "wiki-scraper (for university project | "
    "contact: oskar.rowicki@gmail.com)"
}


def _normalize_phrase(phrase: str) -> str:
    return phrase.strip().replace(" ", "_")


class WikiPage:
    session = requests.Session()
    session.headers.update(HEADERS)

    def __init__(
        self,
        phrase: str | None = None,
        base_url: str = BASE_URL,
        forced_url: str | None = None,
        html_file: str | Path | None = None,
    ):
        self.base_url = base_url.rstrip("/") + "/"

        if html_file:
            self.html_file = Path(html_file)
            self.url = None
            self.phrase = phrase or self.html_file.stem
        else:
            self.html_file = None
            if forced_url:
                self.url = forced_url
                self.phrase = phrase or forced_url.split("/")[-1]
            elif phrase:
                self.phrase = phrase
                self.url = f"{self.base_url}{_normalize_phrase(phrase)}"
                
            else:
                raise ValueError("No phrase, url, or html_file")

        self.soup: BeautifulSoup | None = None
        self.content: Tag | None = None

    def fetch_soup(self) -> BeautifulSoup:
        if self.soup:
            return self.soup

        if self.html_file:
            if not self.html_file.exists():
                raise FileNotFoundError(
                    f"HTML file not found: {self.html_file}"
                )
            text = self.html_file.read_text(encoding="utf-8")
        else:
            if not self.url:
                raise ValueError("No URL available to fetch")
            response = self.session.get(self.url, timeout=10)
            response.raise_for_status()
            text = response.text

        soup = BeautifulSoup(text, "html.parser")

        if soup.select_one(".noarticletext"):
            raise ValueError(
                f"No article found for '{self.phrase}'"
            )

        self.soup = soup
        return soup

    
    def fetch_content(self) -> Tag:
        if self.content:
            return self.content

        soup = self.fetch_soup()
        content = soup.select_one("#mw-content-text .mw-parser-output")
        if not content:
            raise ValueError("No content found")

        self.content = content
        return content

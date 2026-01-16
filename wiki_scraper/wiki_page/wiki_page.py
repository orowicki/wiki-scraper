from pathlib import Path
from collections import Counter

from bs4 import BeautifulSoup, Tag
from pandas import DataFrame

from .fetch import fetch_html
from .info import extract_id_and_title
from .paragraphs import extract_paragraphs
from .links import extract_internal_link_phrases
from .tables import extract_tables
from .word_counts import extract_word_counts

BASE_URL = "https://minecraft.wiki/w/"


class WikiPage:
    def __init__(
        self,
        phrase: str | None = None,
        base_url: str = BASE_URL,
        forced_url: str | None = None,
        html_file: str | Path | None = None,
    ):
        self.base_url = base_url.rstrip("/") + "/"
        self.phrase = None
        self.url = None
        self.html_file = None

        self._html: str | None = None
        self._soup: BeautifulSoup | None = None
        self._content: Tag | None = None

        if html_file:
            self.html_file = Path(html_file)
            self.phrase = phrase or self.html_file.stem
        elif forced_url:
            self.url = forced_url
            self.phrase = phrase or forced_url.split("/")[-1]
        elif phrase:
            self.url = f"{self.base_url}{phrase.strip().replace(' ', '_')}"
            self.phrase = phrase
        else:
            raise ValueError("Must provide phrase, forced_url or html_file")

    def get_html(self) -> str | None:
        if self._html is not None:
            return self._html

        if self.html_file is not None:
            if not self.html_file.exists():
                raise FileNotFoundError(self.html_file)

            html = self.html_file.read_text(encoding="utf-8")
        elif self.url is not None:
            html = fetch_html(self.url)
        else:
            raise RuntimeError("Both 'html_file' and 'url' are somehow None")

        self._html = html
        return html

    def get_soup(self) -> BeautifulSoup | None:
        if self._soup is not None:
            return self._soup

        html = self.get_html()
        if html is None:
            return None

        soup = BeautifulSoup(html, "html.parser")
        if soup.select_one(".noarticletext") is not None:
            return None

        self._soup = soup
        return soup

    def get_content(self) -> Tag | None:
        if self._content is not None:
            return self._content

        soup = self.get_soup()
        if soup is None:
            return None

        content = soup.select_one("#mw-content-text .mw-parser-output")
        if content is None:
            raise RuntimeError(
                "Content container not found - site incompatible?"
            )

        self._content = content
        return content

    def get_info(self) -> tuple[int, str] | None:
        html = self.get_html()
        if html is None:
            return None

        return extract_id_and_title(html)

    def get_paragraphs(self) -> list[Tag] | None:
        content = self.get_content()
        if content is None:
            return None

        return extract_paragraphs(content)

    def get_link_phrases(self) -> set[str] | None:
        content = self.get_content()
        if content is None:
            return None

        return extract_internal_link_phrases(content)

    def get_tables(self) -> list[DataFrame] | None:
        html = self.get_html()
        if html is None:
            return None

        return extract_tables(html)

    def get_word_counts(self) -> Counter | None:
        content = self.get_content()
        if content is None:
            return None

        return extract_word_counts(content)

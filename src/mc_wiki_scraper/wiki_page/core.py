"""
Core module for extracting structured data from Wiki articles.

Provides the ``WikiPage`` class, which handles fetching HTML from a URL
or file, parsing it with BeautifulSoup, and extracting paragraphs,
links, tables, word counts, and article metadata.
"""

from collections import Counter
from pathlib import Path

from bs4 import BeautifulSoup, Tag
from pandas import DataFrame

from .utils import (
    extract_id_and_title,
    extract_internal_link_phrases,
    extract_paragraphs,
    extract_tables,
    extract_word_counts,
    fetch_html,
)


class WikiPage:
    """
    Represents a single Wiki article and provides methods to extract
    content and metadata.

    Parameters
    ----------
    phrase : str, optional
        The article title to fetch (automatically converted to URL).
    base_url : str, default: "https://minecraft.wiki/w/"
        Base URL for the wiki.
    forced_url : str, optional
        Explicit URL to fetch instead of constructing from `phrase`.
    html_file : str or Path, optional
        Path to a local HTML file to read instead of fetching from
        the web.

    Attributes
    ----------
    phrase : str
        Resolved phrase/title of the article.
    url : str | None
        Resolved URL of the article (if any).
    html_file : Path | None
        Path to local HTML file (if any).
    """

    BASE_URL = "https://minecraft.wiki/w/"
    NO_ARTICLE = ".noarticletext"
    CONTENT_TAG = "#mw-content-text .mw-parser-output"

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
        """
        Return the HTML of the page, reading from file or
        fetching from URL.

        Returns
        -------
        str | None
            HTML content, or None if fetching a URL returns 404.
        """
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
        """
        Parse the HTML into a BeautifulSoup object.

        Returns
        -------
        BeautifulSoup | None
            Parsed HTML, or None if the article does not exist.
        """
        if self._soup is not None:
            return self._soup

        html = self.get_html()
        if html is None:
            return None

        soup = BeautifulSoup(html, "html.parser")
        if soup.select_one(self.NO_ARTICLE) is not None:
            return None

        self._soup = soup
        return soup

    def get_content(self) -> Tag | None:
        """
        Return the main content container of the article.

        Returns
        -------
        Tag | None
            BeautifulSoup Tag representing article content, or None if
            missing.
        """
        if self._content is not None:
            return self._content

        soup = self.get_soup()
        if soup is None:
            return None

        content = soup.select_one(self.CONTENT_TAG)
        if content is None:
            raise RuntimeError(
                "Content container not found - site incompatible?"
            )

        self._content = content
        return content

    def get_info(self) -> tuple[int, str] | None:
        """
        Extract the article ID and canonical title from HTML.

        Returns
        -------
        tuple[int, str] | None
            (page_id, page_name) or None if not found.
        """
        html = self.get_html()
        if html is None:
            return None

        return extract_id_and_title(html)

    def get_paragraphs(self) -> list[Tag] | None:
        """
        Extract meaningful paragraphs from the article content.

        Returns
        -------
        list[Tag] | None
            List of <p> Tags, or None if content is missing.
        """
        content = self.get_content()
        if content is None:
            return None

        return extract_paragraphs(content)

    def get_link_phrases(self) -> set[str] | None:
        """
        Extract internal Wiki link phrases from the article content.

        Returns
        -------
        set[str] | None
            Set of linked article phrases, or None if content is
            missing.
        """
        content = self.get_content()
        if content is None:
            return None

        return extract_internal_link_phrases(content)

    def get_tables(self) -> list[DataFrame] | None:
        """
        Extract all HTML tables from the article.

        Returns
        -------
        list[DataFrame] | None
            List of pandas DataFrames representing tables, or
            None if HTML missing.
        """
        html = self.get_html()
        if html is None:
            return None

        return extract_tables(html)

    def get_word_counts(self) -> Counter | None:
        """
        Extract word counts from the article content.

        Returns
        -------
        Counter | None
            Counter of words, or None if content is missing.
        """
        content = self.get_content()
        if content is None:
            return None

        return extract_word_counts(content)

"""
wiki_page
---------
The ``wiki_page`` package provides the ``WikiPage`` class, which
can be instantiated with a URL or HTML file of a Wiki article
and allows for convenient access to view contents of the article in
various ways.
It additionaly exports the namespace of the ``utils`` package.

Functionality:
- inititialize object with URL or HTML file
- parse article with BeautifulSoup
- extract paragraphs
- extract link phrases
- extract tables
- extract word counts
- extract metadata
"""

from . import utils
from .core import WikiPage

__all__ = [
    "WikiPage",
    "utils",
]

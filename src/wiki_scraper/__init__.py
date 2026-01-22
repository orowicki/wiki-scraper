"""
Main package for wiki scraping and analysis.

Provides the top-level Scraper class and exposes submodules for
CLI, article handling, and different modes of operation.
"""

from .cli import Scraper

from . import cli
from . import wiki_page
from . import modes

__all__ = ["Scraper", "cli", "wiki_page", "modes"]

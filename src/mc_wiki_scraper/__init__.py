"""
Main package for wiki scraping and analysis.
---
Provides the top-level Scraper class and exposes submodules for
CLI, article handling, and different modes of operation.
"""

from . import cli, modes, wiki_page
from .cli import Scraper

__all__ = ["Scraper", "cli", "wiki_page", "modes"]

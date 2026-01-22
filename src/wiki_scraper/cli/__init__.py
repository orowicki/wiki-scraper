"""
cli
___
The ``cli`` package provides ways to parse args,
build a mode object from them and run the program.

Functionality:
- parse arguments
- create mode objects from arguments
- create a Scraper class and use it to run the program
"""

from .args import parse_args
from .mode_builder import build_mode
from .scraper import Scraper

__all__ = [
    "parse_args",
    "build_mode",
    "Scraper",
]

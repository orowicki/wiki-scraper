"""
Scraper module for running the program.

Provides the ``Scraper`` class which parses args and builds
the correct mode on initialization, and provides a ``run`` method.
"""

from .args import parse_args
from .mode_builder import build_mode


class Scraper:
    def __init__(self):
        self.args = parse_args()
        self.mode = build_mode(self.args)

    def run(self) -> None:
        self.mode.run()


def main():
    Scraper().run()

if __name__ == "__main__":
    main()

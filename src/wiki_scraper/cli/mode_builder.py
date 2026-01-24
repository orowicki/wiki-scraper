"""
mode builder module for buiding a mode object from args.

Provides the ``build_mode`` function, which returns a mode object
initialized with the right args.
"""

from argparse import Namespace

from ..modes import (
    AnalyzeFrequencyMode,
    AutoCountWordsMode,
    CountWordsMode,
    SummaryMode,
    TableMode,
)
from ..wiki_page import WikiPage


def build_mode(args: Namespace):
    """
    Returns a mode object initialized with passed args.

    Chooses which mode to return based
    on the subparsers arg (args.command).
    """

    match args.command:
        case "summary":
            return SummaryMode(WikiPage(args.phrase))
        case "table":
            return TableMode(WikiPage(args.phrase), args.number)
        case "count-words":
            return CountWordsMode(WikiPage(args.phrase))
        case "auto-count-words":
            return AutoCountWordsMode(
                WikiPage(args.phrase), args.depth, args.wait
            )
        case "analyze-relative-word-frequency":
            return AnalyzeFrequencyMode(args.mode, args.count, args.chart)
        case _:
            raise ValueError("Unknown mode")

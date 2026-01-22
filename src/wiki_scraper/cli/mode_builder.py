"""
mode builder module for buiding a mode object from args.

Provides the ``build_mode`` function, which returns a mode object
initialized with the right args.
"""

from argparse import Namespace

from ..wiki_page import WikiPage
from ..modes import (
    SummaryMode,
    TableMode,
    CountWordsMode,
    AutoCountWordsMode,
    AnalyzeFrequencyMode,
)


def build_mode(args: Namespace):
    """
    Returns a mode object initialized with passed args.

    Assumes args are valid, chooses which mode to return based
    on the args from the mutually exclusive modes group.
    """
    if args.summary:
        return SummaryMode(
            WikiPage(args.summary),
        )
    elif args.table:
        return TableMode(
            WikiPage(args.table),
            args.number,
        )
    elif args.count_words:
        return CountWordsMode(
            WikiPage(args.count_words),
        )
    elif args.auto_count_words:
        return AutoCountWordsMode(
            WikiPage(args.auto_count_words),
            args.depth,
            args.wait,
        )
    elif args.analyze_relative_word_frequency:
        return AnalyzeFrequencyMode(
            args.mode,
            args.count,
            args.chart,
        )
    else:
        raise ValueError("Unknown mode")

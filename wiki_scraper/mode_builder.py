from argparse import Namespace

from wiki_page.wiki_page import WikiPage
from modes.summary import SummaryMode
from modes.table import TableMode
from modes.count_words import CountWordsMode
from modes.auto_count_words import AutoCountWordsMode
from modes.analyze_frequency import AnalyzeFrequencyMode

def build_mode(args: Namespace):
    if args.summary:
        return SummaryMode(
            WikiPage(args.summary),
        )

    if args.table:
        return TableMode(
            WikiPage(args.table),
            args.number,
        )

    if args.count_words:
        return CountWordsMode(
            WikiPage(args.count_words),
        )

    if args.auto_count_words:
        return AutoCountWordsMode(
            WikiPage(args.auto_count_words),
            args.depth,
            args.wait,
        )

    if args.analyze_relative_word_frequency:
        return AnalyzeFrequencyMode(
            args.mode,
            args.count,
            args.chart,
        )

    raise ValueError("Unknown mode")

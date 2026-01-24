"""
args module for parsing CLI arguments and validating them.

Provides the ``parse_args`` function which builds a parser, parses args
and returns the args namespace.
"""

import argparse
import math
from importlib.metadata import version

PROGRAM = "mc-wiki-scraper"
VERSION = version(PROGRAM)


def wait_seconds(value: str) -> float:
    try:
        v = float(value)
    except ValueError:
        raise argparse.ArgumentTypeError("must be a number") from None

    if not math.isfinite(v):
        raise argparse.ArgumentTypeError("must be finite")

    if v < 0:
        raise argparse.ArgumentTypeError("must be non-negative")

    if v > 3600:
        raise argparse.ArgumentTypeError("must be at most 3600 seconds")

    return v


def positive_int(value: str) -> int:
    try:
        v = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError("must be a number") from None

    if v <= 0:
        raise argparse.ArgumentTypeError("must be positive")

    return v


def non_negative_int(value: str) -> int:
    try:
        v = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError("must be a number") from None

    if v < 0:
        raise argparse.ArgumentTypeError("must be non-negative")

    return v


def _add_summary(subparsers):
    parser = subparsers.add_parser(
        "summary",
        help="show the first paragraph of the article",
    )
    parser.add_argument(
        "phrase",
        metavar="PHRASE",
        help="article title to summarize",
    )


def _add_table(subparsers):
    parser = subparsers.add_parser(
        "table",
        help="extract a table from the article and save it to a CSV file",
    )
    parser.add_argument(
        "phrase",
        metavar="PHRASE",
        help="article title to extract table from",
    )
    parser.add_argument(
        "--number",
        type=positive_int,
        required=True,
        metavar="N",
        help="table number (1-based)",
    )


def _add_count_words(subparsers):
    parser = subparsers.add_parser(
        "count-words",
        help="count words in the article and update word-counts.json",
    )
    parser.add_argument(
        "phrase",
        metavar="PHRASE",
        help="article title to counts words in",
    )


def _add_analyze_freq(subparsers):
    parser = subparsers.add_parser(
        "analyze-relative-word-frequency",
        help="compare word frequencies in the articles and in the language",
    )
    parser.add_argument(
        "--mode",
        choices=["article", "language"],
        required=True,
        help="sorting mode",
    )
    parser.add_argument(
        "--count",
        type=positive_int,
        required=True,
        metavar="N",
        help="number of rows to show for relative frequency analysis",
    )
    parser.add_argument(
        "--chart",
        metavar="PATH",
        help="optional output image path for a chart",
    )


def _add_auto_count_words(subparsers):
    parser = subparsers.add_parser(
        "auto-count-words",
        help="automatically follow links in articles and count words in them",
    )
    parser.add_argument(
        "phrase",
        metavar="STARTER_PHRASE",
        help="article title to start following links in",
    )
    parser.add_argument(
        "--depth",
        type=non_negative_int,
        required=True,
        metavar="N",
        help="maximum depth for links",
    )
    parser.add_argument(
        "--wait",
        type=wait_seconds,
        required=True,
        metavar="T",
        help="number of seconds to wait between phrases",
    )


def _build_parser() -> argparse.ArgumentParser:
    """Builds and returns the argument parser for the CLI."""
    parser = argparse.ArgumentParser(
        prog=PROGRAM,
        description="Scrape and analyze pages from minecraft.wiki.",
    )

    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"%(prog)s {VERSION}",
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
        metavar="<mode>",
    )

    _add_summary(subparsers)
    _add_table(subparsers)
    _add_count_words(subparsers)
    _add_analyze_freq(subparsers)
    _add_auto_count_words(subparsers)

    return parser


def parse_args() -> argparse.Namespace:
    """Parse CLI arguments."""
    parser = _build_parser()
    args = parser.parse_args()

    return args


if __name__ == "__main__":
    args = parse_args()
    print(args)

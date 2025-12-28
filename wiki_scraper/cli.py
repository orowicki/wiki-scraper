"""
cli.py
------
Provides a way to parse cli arguments and validate them.

Functions:
- parse_args: builds a parser, parses args, validates them,
              returns the args namespace.
"""

import argparse

__all__ = ["parse_args"]


def _build_parser() -> argparse.ArgumentParser:
    """Builds and returns the argument parser for the CLI."""

    parser = argparse.ArgumentParser(
        prog="wiki_scraper",
        description="Scrape and analyze pages from wiki.",
    )

    # Mutually exclusive program modes
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument(
        "--summary",
        metavar="PHRASE",
        help="Show the first paragraph of the article for PHRASE.",
    )
    modes.add_argument(
        "--table",
        metavar="PHRASE",
        help="Extract a table from the article for PHRASE "
        "and save it to PHRASE.csv.",
    )
    modes.add_argument(
        "--count-words",
        metavar="PHRASE",
        help="Count words in the article for PHRASE "
        "and update word-counts.json.",
    )
    modes.add_argument(
        "--analyze-relative-word-frequency",
        action="store_true",
        help="Compare word frequencies in the article and in the language.",
    )
    modes.add_argument(
        "--auto-count-words",
        metavar="STARTER_PHRASE",
        help="Follow links in articles starting with STARTER_PHRASE "
        "and count words in them.",
    )

    # --table options
    parser.add_argument(
        "--number",
        type=int,
        metavar="N",
        help="Table number when using --table (indexing from 1).",
    )
    parser.add_argument(
        "--first-row-is-header",
        action="store_true",
        default=False,
        help="Treat first row of the table as column headers.",
    )

    # --analyze-relative-word-frequency options
    parser.add_argument(
        "--mode",
        choices=["article", "language"],
        help="Sorting mode for relative frequency analysis.",
    )
    parser.add_argument(
        "--count",
        type=int,
        metavar="N",
        help="Number of rows to show for relative frequency analysis.",
    )
    parser.add_argument(
        "--chart",
        metavar="PATH",
        help="Optional output image path for chart generated via "
        "relative frequency analysis.",
    )

    # --auto-count-words options
    parser.add_argument(
        "--depth",
        type=int,
        metavar="N",
        help="Maximum depth for links during --auto-count-words.",
    )
    parser.add_argument(
        "--wait",
        type=float,
        metavar="T",
        help="Number of seconds to wait between phrases "
        "during --auto-count-words.",
    )

    return parser


def _detect_mode(args: argparse.Namespace) -> str:
    """Returns the chosen mode arg."""

    modes = [
        "summary",
        "table",
        "count_words",
        "analyze_relative_word_frequency",
        "auto_count_words",
    ]

    for m in modes:
        if getattr(args, m, False):
            return m

    raise ValueError("No mode argument provided")


def _check_invalid_args(set_args, allowed_args, mode) -> None:
    """Checks if invalid args for the mode were used."""

    invalid_args = set_args - allowed_args

    if invalid_args:
        invalid_flags = ", ".join(
            f"--{a.replace('_', '-')}" for a in sorted(invalid_args)
        )
        raise ValueError(
            f"Invalid arguments for --{mode.replace('_', '-')}: {invalid_flags}"
        )


def _check_missing_args(set_args, allowed_args, optional_args, mode) -> None:
    """Checks if args are missing for the mode."""

    missing_args = allowed_args - optional_args - set_args

    if missing_args:
        missing_flags = ", ".join(
            f"--{a.replace('_', '-')}" for a in sorted(missing_args)
        )
        raise ValueError(
            f"Missing arguments for --{mode.replace('_', '-')}: {missing_flags}"
        )


def _validate_args(args: argparse.Namespace) -> None:
    """Validates that correct arguments were used for the selected mode."""

    allowed_args = {
        "summary": {"summary"},
        "table": {"table", "number", "first_row_is_header"},
        "count_words": {"count_words"},
        "analyze_relative_word_frequency": {
            "analyze_relative_word_frequency",
            "mode",
            "count",
            "chart",
        },
        "auto_count_words": {"auto_count_words", "depth", "wait"},
    }

    optional_args = {
        "summary": {},
        "table": {"first_row_is_header"},
        "count_words": {},
        "analyze_relative_word_frequency": {"chart"},
        "auto_count_words": {},
    }

    mode = _detect_mode(args)

    set_args = {k for k, v in vars(args).items() if v not in (None, False)}

    _check_invalid_args(set_args, allowed_args[mode], mode)
    _check_missing_args(set_args, allowed_args[mode], optional_args[mode], mode)


def parse_args() -> argparse.Namespace:
    """Parse and validate CLI arguments."""

    parser: argparse.ArgumentParser = _build_parser()
    args: argparse.Namespace = parser.parse_args()
    _validate_args(args)

    return args


if __name__ == "__main__":
    args = parse_args()
    print(args)

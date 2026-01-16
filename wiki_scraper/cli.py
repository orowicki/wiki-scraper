"""
cli.py
------
Provides a way to parse CLI arguments and validate them.

Functions:
- parse_args: builds a parser, parses args, validates them,
              returns the args namespace.
"""

import argparse

__all__ = ["parse_args"]


# Modes mapped to allowed arguments per mode, with `bool required` per arg
MODE_ARGS = {
    "summary": {
        "summary": True,
    },
    "table": {
        "table": True,
        "number": True,
        "first_row_is_header": False,
    },
    "count_words": {
        "count_words": True,
    },
    "analyze_relative_word_frequency": {
        "analyze_relative_word_frequency": True,
        "mode": True,
        "count": True,
        "chart": False,
    },
    "auto_count_words": {
        "auto_count_words": True,
        "depth": True,
        "wait": True,
    },
}


def _build_parser() -> argparse.ArgumentParser:
    """Builds and returns the argument parser for the CLI."""

    parser = argparse.ArgumentParser(
        prog="wiki_scraper",
        description="Scrape and analyze pages from minecraft.wiki.",
        usage=(
            "wiki_scraper.py [-h] <mode> [options]:\n"
            "modes:\n"
            "  --summary PHRASE\n"
            "  --table PHRASE --number N [--first-row-is-header]\n"
            "  --count-words PHRASE\n"
            "  --analyze-relative-word-frequency --mode {article,language} "
            "--count N [--chart PATH]\n"
            "  --auto-count-words STARTER_PHRASE --depth N --wait T"
        ),
    )

    # Mutually exclusive program modes
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument(
        "--summary",
        metavar="PHRASE",
        help="show the first paragraph of the article for PHRASE",
    )
    modes.add_argument(
        "--table",
        metavar="PHRASE",
        help="extract a table from the article for PHRASE "
        "and save it to PHRASE.csv",
    )
    modes.add_argument(
        "--count-words",
        metavar="PHRASE",
        help="count words in the article for PHRASE "
        "and update word-counts.json",
    )
    modes.add_argument(
        "--analyze-relative-word-frequency",
        action="store_true",
        help="compare word frequencies in the article and in the language",
    )
    modes.add_argument(
        "--auto-count-words",
        metavar="STARTER_PHRASE",
        help="follow links in articles starting with STARTER_PHRASE "
        "and count words in them",
    )

    # --table options
    parser.add_argument(
        "--number",
        type=int,
        metavar="N",
        help="table number when using --table (indexing from 1)",
    )
    parser.add_argument(
        "--first-row-is-header",
        action="store_true",
        default=False,
        help="treat first row of the table as column headers",
    )

    # --analyze-relative-word-frequency options
    parser.add_argument(
        "--mode",
        choices=["article", "language"],
        help="sorting mode for relative frequency analysis",
    )
    parser.add_argument(
        "--count",
        type=int,
        metavar="N",
        help="number of rows to show for relative frequency analysis",
    )
    parser.add_argument(
        "--chart",
        metavar="PATH",
        help="optional output image path for chart generated via "
        "relative frequency analysis",
    )

    # --auto-count-words options
    parser.add_argument(
        "--depth",
        type=int,
        metavar="N",
        help="maximum depth for links during --auto-count-words",
    )
    parser.add_argument(
        "--wait",
        type=float,
        metavar="T",
        help="number of seconds to wait between phrases "
        "during --auto-count-words",
    )

    return parser


def _detect_mode(args: argparse.Namespace) -> str:
    """Returns the chosen mode arg."""

    modes = list(MODE_ARGS.keys())

    for m in modes:
        if getattr(args, m, False):
            return m

    raise ValueError("No mode argument provided")


def _check_invalid_args(
    set_args: set[str],
    allowed_args: set[str],
    mode: str,
) -> None:
    """Checks if invalid args for the mode were used."""

    invalid_args = set_args - allowed_args

    if invalid_args:
        invalid_flags = ", ".join(
            f"--{a.replace('_', '-')}" for a in sorted(invalid_args)
        )
        raise ValueError(
            f"Invalid arguments for --{mode.replace('_', '-')}: {invalid_flags}"
        )


def _check_missing_args(
    set_args: set[str],
    required_args: set[str],
    mode: str,
) -> None:
    """Checks if args are missing for the mode."""

    missing_args = required_args - set_args

    if missing_args:
        missing_flags = ", ".join(
            f"--{a.replace('_', '-')}" for a in sorted(missing_args)
        )
        raise ValueError(
            f"Missing arguments for --{mode.replace('_', '-')}: {missing_flags}"
        )


def _validate_args(args: argparse.Namespace) -> None:
    """Validates that correct arguments were used for the selected mode."""

    mode = _detect_mode(args)

    set_args = {k for k, v in vars(args).items() if v not in (None, False)}
    allowed_args = set(MODE_ARGS[mode].keys())
    required_args = {k for k, req in MODE_ARGS[mode].items() if req}

    _check_invalid_args(set_args, allowed_args, mode)
    _check_missing_args(set_args, required_args, mode)


def parse_args() -> argparse.Namespace:
    """Parse and validate CLI arguments."""

    parser = _build_parser()
    args = parser.parse_args()
    _validate_args(args)

    return args


if __name__ == "__main__":
    args = parse_args()
    print(args)

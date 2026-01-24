import argparse

import pytest

from mc_wiki_scraper.cli import args


@pytest.mark.parametrize("val,expected", [(1, 1), (42, 42)])
def test_positive_int_valid(val, expected):
    assert args.positive_int(str(val)) == expected


@pytest.mark.parametrize("val", [0, -1, -42])
def test_positive_int_invalid(val):
    with pytest.raises(argparse.ArgumentTypeError):
        args.positive_int(str(val))


@pytest.mark.parametrize("val,expected", [(0, 0), (10, 10)])
def test_non_negative_int_valid(val, expected):
    assert args.non_negative_int(str(val)) == expected


@pytest.mark.parametrize("val", [-1, -999])
def test_non_negative_int_invalid(val):
    with pytest.raises(argparse.ArgumentTypeError):
        args.non_negative_int(str(val))


@pytest.mark.parametrize("val,expected", [("0", 0.0), ("123.5", 123.5)])
def test_wait_seconds_valid(val, expected):
    assert args.wait_seconds(val) == expected


@pytest.mark.parametrize("val", ["-1", "nan", "inf", "-inf", "3601"])
def test_wait_seconds_invalid(val):
    with pytest.raises(argparse.ArgumentTypeError):
        args.wait_seconds(val)


def test_summary_parsing():
    parser = args._build_parser()
    ns = parser.parse_args(["summary", "Bee"])
    assert ns.command == "summary"
    assert ns.phrase == "Bee"


def test_table_parsing():
    parser = args._build_parser()
    ns = parser.parse_args(["table", "Bee", "--number", "2"])
    assert ns.command == "table"
    assert ns.phrase == "Bee"
    assert ns.number == 2


def test_analyze_freq_parsing():
    parser = args._build_parser()
    ns = parser.parse_args(
        [
            "analyze-relative-word-frequency",
            "--mode",
            "article",
            "--count",
            "5",
        ]
    )
    assert ns.command == "analyze-relative-word-frequency"
    assert ns.mode == "article"
    assert ns.count == 5


def test_auto_count_words_parsing():
    parser = args._build_parser()
    ns = parser.parse_args(
        ["auto-count-words", "Bee", "--depth", "2", "--wait", "1.5"]
    )
    assert ns.command == "auto-count-words"
    assert ns.phrase == "Bee"
    assert ns.depth == 2
    assert ns.wait == 1.5


def test_version_flag():
    parser = args._build_parser()
    with pytest.raises(SystemExit):
        parser.parse_args(["--version"])

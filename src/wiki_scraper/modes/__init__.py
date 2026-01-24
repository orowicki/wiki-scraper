"""
modes
-----
The ``modes`` package provides mode objects that can be ran to perform
their functionality.

Modes:
- ``SummaryMode``:
    print the summary of a Wiki article
- ``TableMode``:
    find a table in a Wiki article, print it, save it to a CSV file
    and print a table of value counts
- ``CountWordsMode``:
    get word counts from a Wiki article and update a JSON file with them
- ``AutoCountWordsMode``:
    explore a Wiki article graph by following links in them, count
    words in every single one and update a JSON file
- ``AnalyzeFrequencyMode``:
    perform relative word frequency analysis, comparing word
    counts from a JSON file and the most common words in a language
"""

from .analyze_frequency import AnalyzeFrequencyMode
from .auto_count_words import AutoCountWordsMode
from .count_words import CountWordsMode
from .summary import SummaryMode
from .table import TableMode

__all__ = [
    "SummaryMode",
    "TableMode",
    "CountWordsMode",
    "AutoCountWordsMode",
    "AnalyzeFrequencyMode",
]

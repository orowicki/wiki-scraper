"""
Table extraction utility for Wiki articles.

Provides a function to extract tables the HTML of a Wiki article and
convert them into pandas DataFrames.
"""

import pandas as pd
import re
from io import StringIO
from html import unescape


def extract_tables(html: str) -> list[pd.DataFrame]:
    """
    Extract all HTML tables into pandas DataFrames.

    The HTML is preprocessed to fix invalid or non-numeric
    ``rowspan`` and ``colspan`` attributes to ensure compatibility with
    ``pandas.read_html``.

    Parameters
    ----------
    html : str
        Raw HTML content.

    Returns
    -------
    list[pandas.DataFrame]
        List of DataFrames parsed from the HTML tables.
    """

    html = unescape(html)

    def fix(match):
        value = match.group(2)
        digits = re.findall(r"\d+", value)
        return f'{match.group(1)}="{digits[0] if digits else "1"}"'

    html = re.sub(r'(colspan|rowspan)\s*=\s*"?([^"> ]*)"?', fix, html)

    return pd.read_html(StringIO(html))

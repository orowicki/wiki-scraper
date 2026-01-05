from bs4 import BeautifulSoup
import pandas as pd
from io import StringIO
import re
from html import unescape


def normalize_spans(html: str) -> str:
    html = unescape(html)

    def fix(match):
        value = match.group(2)
        digits = re.findall(r"\d+", value)
        return f'{match.group(1)}="{digits[0] if digits else "1"}"'

    html = re.sub(r'(colspan|rowspan)\s*=\s*"?([^"> ]*)"?', fix, html)

    return html


def get_table(soup: BeautifulSoup, n: int) -> pd.DataFrame:
    raw_html = str(soup)
    clean_html = normalize_spans(raw_html)

    dsf = pd.read_html(StringIO(clean_html))

    if n > len(dsf):
        raise ValueError(
            f"Table no. {n} doesn't exist in this article, "
            f"highest no. is {len(dsf)}"
        )

    return dsf[n - 1]


def clean_series(series) -> pd.Series:
    series = series.str.strip()
    series = series[series != ""]
    series = series[series.str.lower() != "nan"]
    return series


def get_counts_table(df: pd.DataFrame):
    values = clean_series(pd.Series(df.values.ravel()).astype(str))

    counts = values.value_counts().reset_index()
    counts.columns = ["Value", "Count"]
    return counts


def run_table_mode(phrase: str, soup: BeautifulSoup, n: int) -> None:
    df = get_table(soup, n)
    df.to_csv(f"{phrase}.csv", index=False, encoding="utf-8")
    print(df)

    counts = get_counts_table(df)
    print(f"\nValue counts:\n{counts.to_string(index=False)}")

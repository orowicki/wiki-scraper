"""
Table mode for Wiki articles.

Provides the ``TableMode`` class, which saves a table from a
Wiki article to a CSV file and prints the value counts from the table.
"""

from typing import Any
import pandas as pd
from wiki_page.wiki_page import WikiPage


class TableMode:
    """
    Save a table from a Wiki article to a CSV file and
    print its value counts.

    Parameters
    ----------
    page : WikiPage
        A WikiPage instance representing the article
    table_number : int, optional
        Index of the table in the article (1-based). Defaults to 1
    """

    def __init__(self, page: WikiPage, table_number: int = 1):
        self.page = page
        self.table_number = table_number

    def run(self) -> None:
        """
        Save the selected table to a CSV file and print its value counts.

        If the article has no tables or the table number is out of range,
        an informative message is printed instead.
        """

        tables = self.page.get_tables()
        if tables is None:
            print(f"No tables available for {self.page.phrase}")
            return

        if self.table_number > len(tables):
            print(
                f"Table no. {self.table_number} doesn't exist, "
                f"highest is {len(tables)}."
            )
            return

        df = tables[self.table_number - 1]
        df.to_csv(self._output_path(), index=False, encoding="utf-8")
        print(df)

        counts = self._get_counts_table(df)
        print(f"\nValue counts:\n{counts.to_string(index=False)}")

    def _clean_series(self, series: Any) -> pd.Series:
        series = series.str.strip()
        series = series[series != ""]
        series = series[series.str.lower() != "nan"]
        return series

    def _get_counts_table(self, df: pd.DataFrame) -> pd.DataFrame:
        values = self._clean_series(pd.Series(df.values.ravel()).astype(str))

        counts = values.value_counts().reset_index()
        counts.columns = ["Value", "Count"]
        return counts

    def _output_path(self) -> str:
        return f"{self.page.phrase}.csv"


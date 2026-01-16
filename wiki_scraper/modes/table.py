import pandas as pd
from wiki_page.wiki_page import WikiPage


class TableMode:
    def __init__(self, page: WikiPage, table_number: int = 1):
        self.page = page
        self.table_number = table_number

    def run(self) -> None:
        tables = self.page.get_tables()
        if tables is None:
            return

        if self.table_number > len(tables):
            print(
                f"Table no. {self.table_number} doesn't exist, "
                f"highest is {len(tables)}."
            )
            return

        df = tables[self.table_number - 1]
        df.to_csv(f"{self.page.phrase}.csv", index=False, encoding="utf-8")
        print(df)

        counts = self._get_counts_table(df)
        print(f"\nValue counts:\n{counts.to_string(index=False)}")

    def _clean_series(self, series) -> pd.Series:
        series = series.str.strip()
        series = series[series != ""]
        series = series[series.str.lower() != "nan"]
        return series

    def _get_counts_table(self, df: pd.DataFrame) -> pd.DataFrame:
        values = self._clean_series(pd.Series(df.values.ravel()).astype(str))

        counts = values.value_counts().reset_index()
        counts.columns = ["Value", "Count"]
        return counts

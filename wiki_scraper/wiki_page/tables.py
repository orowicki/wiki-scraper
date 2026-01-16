import pandas as pd
import re
from io import StringIO
from html import unescape


def extract_tables(html: str) -> list[pd.DataFrame]:
    html = unescape(html)

    def fix(match):
        value = match.group(2)
        digits = re.findall(r"\d+", value)
        return f'{match.group(1)}="{digits[0] if digits else "1"}"'

    html = re.sub(r'(colspan|rowspan)\s*=\s*"?([^"> ]*)"?', fix, html)

    return pd.read_html(StringIO(html))

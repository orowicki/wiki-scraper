import io
import sys
from pathlib import Path

from mc_wiki_scraper.modes import SummaryMode
from mc_wiki_scraper.wiki_page.core import WikiPage

HERE = Path(__file__).parent


def test_summary(monkeypatch):
    """
    Integration test: Check functionality of the summary mode on
    a local HTML file.
    """
    html_path = HERE.parent / "test_files" / "Bee.html"

    page = WikiPage(html_file=html_path)
    summary_mode = SummaryMode(page)

    buffer = io.StringIO()

    monkeypatch.setattr(sys, "stdout", buffer)

    summary_mode.run()

    text = buffer.getvalue().strip()

    expected_start = "A bee is a flying arthropodan neutral mob"
    expected_end = (
        "If a bee attacks something, it will lose its stinger and "
        "eventually die."
    )

    assert text.startswith(expected_start), "Output does not start as expected"
    assert text.endswith(expected_end), "Output does not end as expected"

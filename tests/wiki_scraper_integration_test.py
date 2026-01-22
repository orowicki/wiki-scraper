import io
import sys

from wiki_scraper.wiki_page.core import WikiPage
from wiki_scraper.modes import SummaryMode


def main():
    # Load local HTML file instead of fetching from the network
    page = WikiPage(html_file="tests/Bee.html")
    summary_mode = SummaryMode(page)

    # Capture printed output
    buffer = io.StringIO()
    sys.stdout = buffer

    summary_mode.run()

    sys.stdout = sys.__stdout__
    text = buffer.getvalue().strip()

    expected_start = "A bee is a flying arthropodan neutral mob"
    expected_end = "it will lose its stinger and eventually die."

    if not (text.startswith(expected_start) and text.endswith(expected_end)):
        print("Integration test failed!")
        sys.exit(1)

    print("Integration test passed!")


if __name__ == "__main__":
    main()

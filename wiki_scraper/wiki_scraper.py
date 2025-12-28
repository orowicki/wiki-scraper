import cli
import modes.summary
import page_fetcher

args = cli.parse_args()

page = page_fetcher.fetch_page(args.summary)

modes.summary.summarize(page)

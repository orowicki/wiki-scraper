import cli
import modes.summary
import modes.table
import page_fetcher
import modes.count_words
import modes.auto_count_words

args = cli.parse_args()

if args.summary:
    page = page_fetcher.WikiPage(args.summary)
    content = page.fetch_content()
    modes.summary.run_summary(content)
elif args.table:
    page = page_fetcher.WikiPage(args.table)
    soup = page.fetch_soup()
    modes.table.run_table(args.table, soup, args.number)
elif args.count_words:
    page = page_fetcher.WikiPage(args.count_words)
    content = page.fetch_content()
    modes.count_words.run_count_words(content)
elif args.auto_count_words:
    modes.auto_count_words.run_auto_count_words(
        args.auto_count_words, args.depth, args.wait
    )
else:
    raise ValueError("Mode not compatible")

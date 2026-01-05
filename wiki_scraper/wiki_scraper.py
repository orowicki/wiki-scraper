import cli
import modes.summary
import modes.table
import page_fetcher
import modes.count_words

args = cli.parse_args()

page = page_fetcher.fetch_soup(args.table)

modes.table.run_table_mode(args.table, page, args.number)

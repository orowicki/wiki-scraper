import cli
from mode_builder import build_mode


class Scraper:
    def __init__(self, args):
        self.args = args

    def run(self):
        mode = build_mode(self.args)
        mode.run()


if __name__ == "__main__":
    Scraper(cli.parse_args()).run()

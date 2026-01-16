"""
Auto count words mode for Wiki articles.

Provides the ``AutoCountWordsMode`` class, which updates a JSON file with
word counts from a Wiki article then repeats for every internal link found
within it, up to a certain depth.
"""

from modes.count_words import CountWordsMode
from wiki_page.wiki_page import WikiPage
from collections import deque
import time


class AutoCountWordsMode:
    """
    Update a JSON file with word counts from many Wiki articles
    by following links inside them.

    Parameters
    ----------
    root_page : WikiPage
        A WikiPage instance representing the article it starts from
    max_depth : int, optional
        Maximum depth of links to follow. Defaults to 1
    wait : float, optional
        Wait time between article scans. Defaults to 0.1
    """

    def __init__(
        self, root_page: WikiPage, max_depth: int = 1, wait: float = 0.1
    ):
        self.root_page = root_page
        self.max_depth = max_depth
        self.wait = wait

        self.queue: deque[tuple[str, int]] = deque()
        self.visited_ids: set[int] = set()
        self.seen_phrases: set[str] = set()

    def run(self) -> None:
        """
        Update a JSON file with word counts from every article it encounters.

        Starts from the root article and explores internal links in it and every
        subsequent article until max depth is reached.

        If the root article has no content, an informative message is printed
        instead.
        """

        root_info = self.root_page.get_info()
        if root_info is None:
            print(f"No article available for '{self.root_page.phrase}'")
            return

        root_title = root_info[1]
        self.queue.append((root_title, 0))
        self.seen_phrases.add(root_title)

        while self.queue:
            self._process_phrase()
            time.sleep(self.wait)

    def _process_phrase(self) -> None:
        phrase, depth = self.queue.popleft()
        page = WikiPage(phrase)

        info = page.get_info()
        if info is None:
            return

        page_id, title = info
        if page_id in self.visited_ids:
            return

        content = page.get_content()
        if content is None:
            print(f"No content in {title} - skipping")
            return

        self.visited_ids.add(page_id)
        print(title)
        CountWordsMode(page).run()

        if depth < self.max_depth:
            self._enqueue_links(page, depth)

    def _enqueue_links(self, page: WikiPage, depth: int) -> None:
        link_phrases = page.get_link_phrases()
        if link_phrases is None:
            return

        for phrase in link_phrases:
            if phrase not in self.seen_phrases:
                self.seen_phrases.add(phrase)
                self.queue.append((phrase, depth + 1))

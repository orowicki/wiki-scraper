import json

from bs4 import BeautifulSoup

from mc_wiki_scraper.wiki_page.utils import extract_word_counts, fetch_html

ENGLISH_MOBY_DICK_LINK = (
    "https://www.gutenberg.org/files/2701/2701-h/2701-h.htm#link2HCH0028"
)

POLISH_MACHIAVELLI_THE_PRINCE_LINK = (
    "https://wolnelektury.pl/katalog/lektura/"
    "machiavelli-traktat-o-ksieciu.html"
)

SPANISH_LA_VIDA_DE_LAZARILLO_LINK = (
    "https://www.gutenberg.org/ebooks/320.txt.utf-8"
)


# (Need to manually change the value of link)
def main():
    link = SPANISH_LA_VIDA_DE_LAZARILLO_LINK
    html = fetch_html(link)

    if html is None:
        raise RuntimeError

    if link == SPANISH_LA_VIDA_DE_LAZARILLO_LINK:
        start = html.find(
            "*** START OF THE PROJECT GUTENBERG EBOOK VIDA DE LAZARILLO "
            "DE TORMES Y DE SUS FORTUNAS Y ADVERSIDADES ***"
        )
        end = html.find(
            "*** END OF THE PROJECT GUTENBERG EBOOK VIDA DE "
            "LAZARILLO DE TORMES Y DE SUS FORTUNAS Y ADVERSIDADES ***"
        )
        html = html[start:end]

    soup = BeautifulSoup(html, "html.parser")

    counts = extract_word_counts(soup)

    with open("word-counts.json", "w", encoding="utf-8") as f:
        json.dump(counts, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from wordfreq import top_n_list, zipf_frequency
import json

WORD_COUNTS = "word-counts.json"
LANG = "en"
LANGUAGE = "English"
MAX_LANG_WORDS = 10_000


def load_word_counts() -> dict[str, int]:
    with open(WORD_COUNTS, "r", encoding="utf-8") as f:
        return json.load(f)


def get_normalized_article_counts(
    word_counts: dict[str, int],
) -> dict[str, float]:
    if not word_counts:
        raise ValueError("Empty word counts")

    max_freq = max(word_counts.values())
    return {word: count / max_freq for word, count in word_counts.items()}


def get_normalized_lang_counts() -> dict[str, float]:
    lang_words = top_n_list(LANG, MAX_LANG_WORDS)
    lang_zipf = {w: zipf_frequency(w, LANG) for w in lang_words}
    lang_max = max(lang_zipf.values())
    return {word: freq / lang_max for word, freq in lang_zipf.items()}


def get_table_article_mode(
    article_norms,
    lang_norms,
    count: int,
) -> pd.DataFrame:
    rows = []

    top_articles = sorted(
        article_norms.items(),
        key=lambda x: x[1],
        reverse=True,
    )[:count]

    for word, freq in top_articles:
        rows.append(
            {
                "word": word,
                "frequency in the article": freq,
                "frequency in wiki language": lang_norms.get(word, np.nan),
            }
        )

    return pd.DataFrame(rows)


def get_table_lang_mode(
    article_norms,
    lang_norms,
    count: int,
) -> pd.DataFrame:
    rows = []

    top_lang = sorted(
        lang_norms.items(),
        key=lambda x: x[1],
        reverse=True,
    )[:count]

    for word, freq in top_lang:
        rows.append(
            {
                "word": word,
                "frequency in the article": article_norms.get(word, np.nan),
                "frequency in wiki language": freq,
            }
        )

    return pd.DataFrame(rows)


def plot_frequency_comparison(
    table: pd.DataFrame,
    path: str,
    mode: str,
):
    words = table["word"].astype(str).tolist()
    article_freqs = table["frequency in the article"].fillna(0).to_numpy()
    lang_freqs = table["frequency in wiki language"].fillna(0).to_numpy()

    x = np.arange(len(words))
    width = 0.4

    plt.figure(figsize=(max(10, len(words) * 0.6), 6))

    plt.bar(
        x - width / 2,
        article_freqs,
        width,
        label="Wiki",
    )
    plt.bar(
        x + width / 2,
        lang_freqs,
        width,
        label=LANGUAGE,
    )

    plt.xticks(x, words, rotation=45, ha="right")
    plt.ylabel("Normalized frequency")
    plt.xlabel("Word")
    plt.title(f"Word frequency comparison ({mode} mode)")
    plt.legend()

    plt.tight_layout()
    plt.savefig(path)
    plt.close()


def run_analyze_frequency(mode: str, count: int, path: str | None = None):
    word_counts = load_word_counts()
    article_norms = get_normalized_article_counts(word_counts)
    lang_norms = get_normalized_lang_counts()

    if mode == "article":
        table = get_table_article_mode(article_norms, lang_norms, count)
    elif mode == "language":
        table = get_table_lang_mode(article_norms, lang_norms, count)
    else:
        raise ValueError("mode must be 'article' or 'language'")

    print(table)

    if path:
        plot_frequency_comparison(table, path, mode)

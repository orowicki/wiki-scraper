"""
Analyze relative word frequency mode for Wiki articles.

Provides the ``AnalyzeFrequencyMode`` class, which loads word
frequency data collected from Wiki articles, normalizes it, and compares it
against frequency data from a reference language. Results can be displayed
as tables and optionally visualized as charts.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from wordfreq import top_n_list, zipf_frequency
import json


class AnalyzeFrequencyMode:
    """
    Analyze and compare word frequencies from Wiki articles and a language.

    The analysis can be performed in two modes:
    - ``article``: focus on the most frequent words in the article
    - ``language``: focus on the most frequent words in the language

    Frequencies are normalized and presented in tabular form. Optionally,
    a bar chart comparing article and language frequencies can be generated.

    Parameters
    ----------
    mode : str
        Analysis mode. Must be either ``'article'`` or ``'language'``
    count : int
        Number of words to include in the output
    chart_path : str or None, optional
        Path to save the comparison chart. If ``None``, no chart is generated
    """

    WORD_COUNTS_FILE = "word-counts.json"
    LANG = "en"
    LANGUAGE_NAME = "English"
    MAX_LANG_WORDS = 10_000

    def __init__(self, mode: str, count: int, chart_path: str | None = None):
        self.mode = mode
        self.count = count
        self.chart_path = chart_path

        self.word_counts: dict[str, int] = {}
        self.article_norms: dict[str, float] = {}
        self.lang_norms: dict[str, float] = {}

    def run(self):
        """
        Perform the frequency analysis and display the results.

        Loads word counts from a JSON file, normalizes article and language
        frequencies,and produces a comparison table according to the
        selected mode.
        The table is printed to standard output.

        If a chart path was provided, a bar chart visualizing the comparison
        is also generated and saved.
        """

        self.load_word_counts()
        self.normalize_article_counts()
        self.normalize_lang_counts()

        if self.mode == "article":
            table = self._get_table_article_mode()
        elif self.mode == "language":
            table = self._get_table_lang_mode()
        else:
            raise ValueError("mode must be 'article' or 'language'")

        print(table)
        if self.chart_path is not None:
            self.plot_comparison(table)

    def load_word_counts(self):
        """
        Load word count data from a JSON file.

        The file is expected to contain a mapping from words to their occurrence
        counts in Wiki articles.
        """

        with open(self.WORD_COUNTS_FILE, "r", encoding="utf-8") as f:
            self.word_counts = json.load(f)

    def normalize_article_counts(self):
        """
        Normalize word frequencies from the article.

        Frequencies are normalized by dividing each count by the maximum
        word frequency found in the article.
        """

        if self.word_counts is None:
            raise ValueError("Empty word counts")
        max_freq = max(self.word_counts.values())
        self.article_norms = {
            w: c / max_freq for w, c in self.word_counts.items()
        }

    def normalize_lang_counts(self):
        """
        Normalize word frequencies for the reference language.

        Word frequencies are obtained using Zipf frequency values for the most
        common words in the selected language and normalized by the maximum
        Zipf frequency.
        """

        lang_words = top_n_list(self.LANG, self.MAX_LANG_WORDS)
        lang_zipf = {w: zipf_frequency(w, self.LANG) for w in lang_words}
        lang_max = max(lang_zipf.values())
        self.lang_norms = {w: f / lang_max for w, f in lang_zipf.items()}

    def plot_comparison(self, table: pd.DataFrame):
        """
        Generate and save a bar chart comparing word frequencies.

        The chart compares normalized word frequencies from the article and
        the reference language for the words listed in the provided table.

        Parameters
        ----------
        table : pandas.DataFrame
            DataFrame containing words and their normalized frequencies.
        """

        words = table["word"].astype(str).tolist()
        article_freqs = table["frequency in the article"].fillna(0).to_numpy()
        lang_freqs = table["frequency in wiki language"].fillna(0).to_numpy()
        x = np.arange(len(words))
        width = 0.4

        plt.figure(figsize=(max(10, len(words) * 0.6), 6))
        plt.bar(x - width / 2, article_freqs, width, label="Wiki")
        plt.bar(x + width / 2, lang_freqs, width, label=self.LANGUAGE_NAME)
        plt.xticks(x, words, rotation=45, ha="right")
        plt.ylabel("Normalized frequency")
        plt.xlabel("Word")
        plt.title(f"Word frequency comparison ({self.mode} mode)")
        plt.legend()
        plt.tight_layout()
        plt.savefig(self.chart_path)
        plt.close()

    def _get_table_article_mode(self) -> pd.DataFrame:
        rows = []
        for word, freq in sorted(
            self.article_norms.items(), key=lambda x: x[1], reverse=True
        )[: self.count]:
            rows.append(
                {
                    "word": word,
                    "frequency in the article": freq,
                    "frequency in wiki language": self.lang_norms.get(
                        word, np.nan
                    ),
                }
            )

        return pd.DataFrame(rows)

    def _get_table_lang_mode(self) -> pd.DataFrame:
        rows = []
        for word, freq in sorted(
            self.lang_norms.items(), key=lambda x: x[1], reverse=True
        )[: self.count]:
            rows.append(
                {
                    "word": word,
                    "frequency in the article": self.article_norms.get(
                        word, np.nan
                    ),
                    "frequency in wiki language": freq,
                }
            )

        return pd.DataFrame(rows)

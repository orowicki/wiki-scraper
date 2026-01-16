import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from wordfreq import top_n_list, zipf_frequency
import json


class AnalyzeFrequencyMode:
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
        with open(self.WORD_COUNTS_FILE, "r", encoding="utf-8") as f:
            self.word_counts = json.load(f)

    def normalize_article_counts(self):
        if self.word_counts is None:
            raise ValueError("Empty word counts")
        max_freq = max(self.word_counts.values())
        self.article_norms = {
            w: c / max_freq for w, c in self.word_counts.items()
        }

    def normalize_lang_counts(self):
        lang_words = top_n_list(self.LANG, self.MAX_LANG_WORDS)
        lang_zipf = {w: zipf_frequency(w, self.LANG) for w in lang_words}
        lang_max = max(lang_zipf.values())
        self.lang_norms = {w: f / lang_max for w, f in lang_zipf.items()}

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

    def plot_comparison(self, table: pd.DataFrame):
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

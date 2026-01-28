# %% [markdown]
# # Analiza skuteczności funkcji wykrywającej język

# %% [markdown]
# ## Importy

# %%
import json
from collections import Counter
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
from wordfreq import top_n_list

# %% [markdown]
# ## Ładujemy przygotowane dane

# %%
word_count_files = {
    "wiki_long": "word_counts/long_article/word-counts.json",
    "wiki_bad": "word_counts/bad_article/word-counts.json",
    "english_long": "word_counts/english/word-counts.json",
    "polish_long": "word_counts/polish/word-counts.json",
    "spanish_long": "word_counts/spanish/word-counts.json",
}

word_counts_data = {}
for name, path in word_count_files.items():
    with open(path, encoding="utf-8") as f:
        word_counts_data[name] = json.load(f)

# %% [markdown]
# ## Ładujemy dane o językach

# %%
languages = {
    "english": top_n_list("en", 1000, wordlist="large"),
    "polish": top_n_list("pl", 1000, wordlist="large"),
    "spanish": top_n_list("es", 1000, wordlist="large"),
}

languages_ranked = {}
for lang, words in languages.items():
    languages_ranked[lang] = {w: rank + 1 for rank, w in enumerate(words)}

# %% [markdown]
# ## Definicja funkcji określania pewności co do języka


# %%
def lang_confidence_score(
    word_counts: dict[str, int], lang_words_with_rank: dict[str, int]
) -> float:
    """
    Compute a language confidence score for a text.

    Higher score = better match with the language.

    Params
    ------
        word_counts: dict[word -> count]
        lang_words_with_rank: dict[word -> rank] (1 = most frequent)
    """
    score = 0.0
    for word, count in word_counts.items():
        rank = lang_words_with_rank.get(word, None)
        if rank is not None:
            # Inverse rank weighting: higher score for frequent words
            score += count / rank
    return score


# %% [markdown]
# ## Liczymy wyniki dla 3, 10, 100, 1000 słów.

# %%
k_values = [3, 10, 100, 1000]
results = {}

for k in k_values:
    results[k] = {}
    for lang, ranks in languages_ranked.items():
        # Use only top k words
        topk = {w: r for w, r in ranks.items() if r <= k}
        scores = {}
        for text_name, wc in word_counts_data.items():
            scores[text_name] = lang_confidence_score(wc, topk)
        results[k][lang] = scores

# %% [markdown]
# ## Rysujemy wykresy dla wyników

# %%
texts = list(word_counts_data.keys())
for k in k_values:
    plt.figure(figsize=(10, 4))
    for lang in languages_ranked.keys():
        y = [results[k][lang][txt] for txt in texts]
        plt.plot(texts, y, marker="o", label=lang)
    plt.title(f"Language confidence score for top-{k} words")
    plt.xlabel("Text / Article")
    plt.ylabel("Confidence score")
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.show()




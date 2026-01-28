# %% [markdown]
# # Analiza skuteczności funkcji wykrywającej język

# %% [markdown]
# ## Importy

# %%
import json

import matplotlib.pyplot as plt
from wordfreq import top_n_list, word_frequency

# %% [markdown]
# ## Ładujemy przygotowane dane o tekstach/artykułach

# %%
word_count_files = {
    "Wiki długi": "word_counts/long_article/word-counts.json",
    "Wiki słaby": "word_counts/bad_article/word-counts.json",
    "Moby Dick (angielski)": "word_counts/english/word-counts.json",
    "Książe (polski)": "word_counts/polish/word-counts.json",
    "Vida De Lazarillo.. (hiszpański)": "word_counts/spanish/word-counts.json",
}

word_counts_data = {}
for name, path in word_count_files.items():
    with open(path, encoding="utf-8") as f:
        word_counts_data[name] = json.load(f)

# %% [markdown]
# ## Przygotowujemy dane o językach

# %%
languages = {
    "angielski": ("en", top_n_list("en", 1000, wordlist="large")),
    "polski": ("pl", top_n_list("pl", 1000, wordlist="large")),
    "hiszpański": ("es", top_n_list("es", 1000, wordlist="large")),
}

languages_with_word_frequencies = {}
for lang, (code, words) in languages.items():
    languages_with_word_frequencies[lang] = {
        w: word_frequency(w, code) for w in words
    }

# %% [markdown]
# ## Definicja funkcji określania pewności co do języka


# %%
def lang_confidence_score(
    word_counts: dict[str, int], lang_words_with_freq: dict[str, int]
) -> float:
    """
    Compute a language confidence score for a text.

    Higher score = better match with the language.

    Parameters
    ----------
    word_counts: dict[word -> count]
    lang_words_with_freq: dict[word -> frequency]
    """
    max_freq = max(lang_words_with_freq.values())
    words_with_normalized_freq = {
        w: freq / max_freq for w, freq in lang_words_with_freq.items()
    }

    score = 0.0
    for word, count in word_counts.items():
        frequency = words_with_normalized_freq.get(word, 0)
        score += frequency * count

    score /= sum(word_counts.values())
    return score


# %% [markdown]
# ## Liczymy wyniki dla 3, 10, 100, 1000 najczęstszych słów w językach

# %%
k_values = [3, 10, 100, 1000]
results = {}

for k in k_values:
    results[k] = {}
    for lang, frequencies in languages_with_word_frequencies.items():
        topk = {
            w: freq for r, (w, freq) in enumerate(frequencies.items()) if r < k
        }
        scores = {}
        for text_name, wc in word_counts_data.items():
            scores[text_name] = lang_confidence_score(wc, topk)
        results[k][lang] = scores

# %% [markdown]
# ## Rysujemy wykresy dla wyników

# %%
texts = list(word_counts_data.keys())
for k in k_values:
    plt.figure(figsize=(12, 5))
    for lang in languages.keys():
        y = [results[k][lang][txt] for txt in texts]
        plt.plot(texts, y, marker="o", label=lang)
    plt.title(f"Wynik pewności języka dla {k} najczęstszych słów")
    plt.xlabel("Tekst / Artykuł")
    plt.ylabel("Wynik")
    plt.legend()
    plt.tight_layout()
    plt.show()


# %% [markdown]

# ## Analiza wyników
#
# Funkcja `lang_confidence_score` jest dość skuteczna.
# Dla każdej ze sprawdzanych wielkości `k`, wynik dla języka źródłowego
# był znacznie większy od wyników dla innych języków.
#
# Podczas, gdy różnica wyników dla `k = 3` i `k = 10` jest duża,
# wraz ze wzrostem `k`, różnica między wynikami szybko maleje -
# wykresy dla `k = 100` i `k = 1000` są niemal takie same.
# Jest to najprawdopodobniej spowodowane heurystyką przedstawionej
# funkcji, która licząc wynik silnie faworyzuje te słowa, które
# występują najczęściej, zatem ignorowanie rzadziej występujących słów
# nie ma dużego wpływu na wynik.
#
# Maksymalny wynik, który może zwrócić `lang_confidence_score` to `1.0`,
# ale przedstawione wyniki nie przekraczają `0.16`. Jest tak dlatego, że
# wynik `1.0` jest możliwy tylko dla tekstów składających się całkowicie
# z najczęstszego słowa w danym języku. Z tych powodów możliwe, że
# dla analizy realistycznych tekstów warto by było normalizować jakoś
# wynik, np. dzieląc przez `0.18`, i odczytując go jako `%` pewności.
#
# Dobór języków miał znaczenie. Dla języka polskiego funkcja zadziałała
# najgorzej, podczas gdy dla hiszpańskiego najlepiej.
# Można z tego wywnioskować, że funkcja prawdopodobnie działa lepiej
# dla języków mniej fleksyjnych + o bardziej ustalonym szyku zdania.
#
# Ponieważ funkcja daje niższy wynik dla bardziej fleksyjnych języków,
# możnaby zastosować heurystykę, że niższy wynik dla języka i tekstu
# w nim napisanego, względem takich wyników innych języków, oznacza, że
# w danym języku słowa są częściej odmieniane.
#
# Znalezienie artykułu, który daje słaby wynik nie było trudne.
# Celowałem w stosunkowo krótki artykuł o rzeczy nieistniejącej
# w języku angielskim. Wygrał `Netherite_sword`, w którego
# artykule często występują słowa "netherite"
# (które nie istnieje w angielskim) oraz "sword"
# (które raczej nie jest częstym słowem w angielskim).
# Gdyby wybrane wiki nie było o grze wideo, możliwe, że nie istniałby
# artykuł pełny fikcyjnego słowa.

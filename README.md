# MC Wiki Scraper

![Python](https://img.shields.io/pypi/pyversions/mc-wiki-scraper)
![Tests](https://img.shields.io/github/workflow/status/orowicki/wiki-scraper/Tests)
![Coverage](https://img.shields.io/codecov/c/github/orowicki/wiki-scraper)
![Lint](https://img.shields.io/badge/lint-ruff-green)
![PyPI](https://img.shields.io/pypi/v/mc-wiki-scraper)

Scrape and analyze articles from [minecraft.wiki](https://minecraft.wiki/).

---

## Features

- **Summary** – Get the first paragraph of an article.
- **Table Extraction** – Extract tables and save them as CSV.
- **Count Words** – Count words in an article and aggregate results in `word-counts.json`.
- **Analyze Relative Word Frequency** – Compare word frequencies across articles or the whole language.
- **Auto Count Words** – Traverse links automatically and count words in articles.

---

## Usage

```bash
mc-wiki-scraper -h
```

---

## Installation

Requires **Python 3.13+**. Install to a virtual environment (recommended):

```bash
pip install mc-wiki-scraper
```

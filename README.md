# MC Wiki Scraper

![Python](https://img.shields.io/pypi/pyversions/mc-wiki-scraper)
[![PyPI](https://img.shields.io/pypi/v/mc-wiki-scraper)](https://pypi.org/project/mc-wiki-scraper/)
[![Tests](https://img.shields.io/github/actions/workflow/status/orowicki/wiki-scraper/tests)](https://github.com/orowicki/wiki-scraper/actions)
![Lint](https://img.shields.io/badge/lint-ruff-green)

Scrape and analyze articles from [minecraft.wiki](https://minecraft.wiki/)

---

## Features

- **Summary** – Get the first paragraph of an article.  
- **Table Extraction** – Extract tables and save them as CSV.  
- **Count Words** – Count words in an article and aggregate results in `word-counts.json`.  
- **Analyze Relative Word Frequency** – Compare word frequencies across articles or the whole language.  
- **Auto Count Words** – Traverse links automatically and count words in articles.  

---

## Usage

Show help:

```bash
mc-wiki-scraper -h
```

Example:

```bash
mc-wiki-scraper summary 'iron ingot'
```

---

## Installation

Requires **Python 3.11+**. Install to a virtual environment (recommended):

```bash
python -m venv .venv  
source .venv/bin/activate  
pip install mc-wiki-scraper
```

---

## Development

Clone the repository and install with test dependencies:
```bash
pip install -e '.[test]'  
pytest
```

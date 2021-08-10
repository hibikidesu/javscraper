# javscraper
Scraper library for JAVs.

## Supported Sites
- R18
- JAVLibrary
- MGStage
- S1
- SOD Prime
- 10Musume
- IdeaPocket
- Caribbeancom

## Requirements
- python3.4+

## Installation
```commandline
python -m pip install -U javscraper
```

## Usage
```python
>>> from javscraper import *
>>> javlibrary = JAVLibrary()

# Searching for videos
>>> print(javlibrary.search("SSIS-001"))
[...]

# Getting video data
>>> print(javlibrary.get_video("SSIS-001"))
JAVResult(name=..., code=..., studio=..., ...)
```
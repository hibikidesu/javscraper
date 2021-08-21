# javscraper
Scraper library for JAVs.

## Supported Sites
- AirControl
- AliceJapan
- Aroma
- Attackers
- Aurora Project
- BeFree
- Bi
- Big Morkal
- Caribbeancom
- Deeps
- DMM
- Heyzo
- IdeaPocket
- JAVLibrary
- KMProduce
- Max-A
- MGStage
- R18
- S1
- SOD Prime
- 1pondo
- 10Musume

## Requirements
- python3.7+

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
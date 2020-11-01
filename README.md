# Web Scraping

I often do webscraping projects for personal project, to help friends, and for freelancing. Up to this point I have been disorganied on this, so I wanted to start writing better code for reusability.

I will include any scraper classes that I don't mind sharing but will keep certain scrapers private.

The main entry point is `main.py` where can see the example of running the scraper and writing the data out to `.xlsx`.
In `helpers/`:

- `base_scraper.py` - the scraping base class. Shows that you need to implement to `parse_soup` method, which will be unique for different domains.
- `writer.py` - class and interface for writing data out to a file.

## Installation

[poetry][1] is used aspackage manager, please install then you can run `poetry install`

[1]: https://python-poetry.org/

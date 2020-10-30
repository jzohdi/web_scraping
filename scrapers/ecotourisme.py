from bs4 import BeautifulSoup
from requests import get
import re
from scraper import WriterHelper
from helpers.writer import XLWriter
from helpers.base_scraper import BaseScraper


class Scraper(BaseScraper):
    def __init__(self, base_url):
        super().__init__(base_url)
        
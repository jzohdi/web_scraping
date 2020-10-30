from bs4 import BeautifulSoup
from requests import get


class BaseScraper:
    def __init__(self, base_url):
        self.url = base_url
        self.cache = set()

    def save_visit(self, hashable_key):
        self.cache.add(hashable_key)

    def was_processed(self, hashable_key):
        return hashable_key in self.cache

    def request_page(self, endpoint, callback):

        response = get(self.url + endpoint)
        if response.status_code == 200:
            soup = self.get_soup(response)
            return callback(soup)
        return False

    def get_soup(self, response):
        content = response.content
        return BeautifulSoup(content, "html.parser")

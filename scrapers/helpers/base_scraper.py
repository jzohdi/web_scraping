from bs4 import BeautifulSoup
from requests import get

class BaseScraper:
    def __init__(self, base_url):
        self.url = base_url

    @staticmethod
    def request_page(endpoint: str):
        response = get(endpoint)
        if response.status_code == 200:
            return response.content
        return None

    @staticmethod
    def get_soup(content):
        return BeautifulSoup(content, "html.parser")

    def run(self):
        content = self.request_page(self.url)
        if content is not None:
            soup = self.get_soup(content)
            return self.parse_soup(soup)
        return None

    """ implement this method. returns the final data in some form """
    def parse_soup(self, soup): raise NotImplementedError
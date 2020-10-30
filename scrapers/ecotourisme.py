from bs4 import BeautifulSoup
from requests import get
import re
from .helpers.writer import WriterHelper
from .helpers.base_scraper import BaseScraper


class Scraper(BaseScraper):
    def __init__(self, base_url):
        super().__init__(base_url)
        self.url = base_url

    def parse_soup(self, soup):
        content_container = soup.find(id="cc-matrix-2200712593")
        # sections = self.find_ele_contains(content_container, "div", "class", "j-textWithImage")
        sections = content_container.find_all("div", class_="j-textWithImage")
        
        all_data = []
        for section in sections:
            data =  self.parse_section(section)
            all_data.append(data)

        return all_data

    def parse_section(self, soup_section):
        container = soup_section.find("div").find("div")
        text = container.getText()
        formatted = re.sub(' +', ' ', text)
        split = formatted.split("\n")
        remove_empty_items = list(filter(lambda x: self.isValidItem(x), split))
        return remove_empty_items


    def isValidItem(self, item):
        if len(item) == 0:
            return False
        if len(item) == 1:
            return False
        if item == ' \xa0':
            return False
        return True
    
    """ parses and returns dictionary of items """
    # def parse_section(self, soup_section):
    #     container = soup_section.find("div").find("div")
    #     text = container.getText()
    #     formatted = re.sub(' +', ' ', text)
    #     split = formatted.split("\n")
    #     header = split[2]
    #     owner = split[5]
    #     address = split[9] + split[10]
    #     phone = split[11]
    #     email_site = split[12]
    #     rest = ' '.join(split[13:])

    #     return { 
    #         "name": header,
    #         "owner": owner,
    #         "address": address,
    #         "phone": phone,
    #         "contact": email_site, 
    #         "details": rest
    #         }
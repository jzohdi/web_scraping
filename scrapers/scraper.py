from bs4 import BeautifulSoup
from requests import get
import re
from excel_writer import XLWriter


class Parser:
    def __init__(self, location_string=None):
        self.url = "https://procontact.afnor.org"
        self.search = "/recherche/?mot={0}" + location_string + "&page="
        self.all = []
        self.cache = set()

    def visited(self, result):
        unique = result["name"] + result["address"]
        self.cache.add(unique)

    def was_processed(self, result):
        unique = result["name"] + result["address"]
        return unique in self.cache

    def make_request(self, search_word, num):
        response = get(self.url + self.search.format(search_word) + num)
        if response.status_code == 200:
            return self.build_quotes(response)
        else:
            return False

    def request_page(self, link):

        response = get(self.url + link)
        if response.status_code == 200:
            soup = self.get_soup(response)
            return self.scrape_page(soup)

        return False

    def get_soup(self, response):
        content = response.content
        return BeautifulSoup(content, "html.parser")

    def build_quotes(self, response):
        soup = self.get_soup(response)
        return self.find_links(soup)

    def find_links(self, soup):
        list_of_sites = soup.find_all("li", {"class": "bloc-tbl-row"})

        if len(list_of_sites) == 0:
            return False

        for site in list_of_sites:
            certificate = site.find(
                "div",
                {
                    "style": "background-image: url('https://www.espaceclient-certification.afnor.org/images/Ressources/ecd16908-15f7-4437-b4d9-ec628ca6f78d.png')"
                },
            )
            if certificate != None:
                link = site.find("a", href=True)
                self.all.append(link["href"])
            else:
                print("no eco label found")

        return True

    def scrape_page(self, soup):
        final = {}
        info = soup.find("div", {"class": "bloc-tbl intro"})
        final = self.type_and_address(info.getText().strip().split("\n"))
        more_info = soup.find("div", {"class": "bloc-links-com"}).find_all("li")
        final["info"] = " ".join([more.getText() for more in more_info])
        characteristics = soup.find("div", {"id": "blocTxt_2"})
        final["Characteristiques"] = (
            characteristics.getText().strip().replace("Caractéristiques :", "")
        )
        return final

    def type_and_address(self, text_list):

        text_list = self.remove_empty_string(text_list)
        data = {}
        data["type"] = text_list.pop(0)
        data["name"] = text_list.pop(0)
        # address will be the rest of the list
        data["address"] = ", ".join(text_list)
        return data

    def remove_empty_string(self, text_list):
        return [item for item in text_list if item.strip() != ""]


if __name__ == "__main__":

    xl_helper = WriterHelper(1, XLWriter())
    xlsheet_header = [
        "Index",
        "Type",
        "Name",
        "Address",
        "Infomation",
        "Characteristiques",
    ]
    xl_helper.init_xl(xlsheet_header)

    france_location_string = "&adresse=france&latitude=32.5287806&longitude=-117.0277194&orderBy=?mot=hotels&adresse=france&latitude=46.227638&longitude=2.213749&orderBy="
    parser = Parser(france_location_string)
    # do this for each page

    search_words = ["hotels", "camping"]
    for keyword in search_words:
        n = 1
        while parser.make_request("hotels", str(n)):
            n += 1

    if parser.all:
        for page in parser.all:
            result = parser.request_page(page)
            if not parser.was_processed(result):
                xl_helper.add_row(result)
                parser.visited(result)

    xl_helper.save("Afnor Eco Locations")

# for n in range(120)
#     print("currently processing: ", str(n))
#     parser.make_request(str(n))
# parser.make_request('1')
# parser.write_to_file()

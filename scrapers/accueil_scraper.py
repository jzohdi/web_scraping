from bs4 import BeautifulSoup
from requests import get
import re
from scraper import WriterHelper
from excel_writer import XLWriter
from base_scraper import BaseScraper


class Accueil(BaseScraper):
    def __init__(self, base_url):
        super().__init__(base_url)
        self.links = []
        self.success = True

    def scrape_page(self, soup):
        self.success = False
        ul = soup.find("ul", {"class": "list_container"})
        links_list = ul.find_all("a", href=True)
        for a in links_list:
            self.links.append(a["href"])
            self.success = True

    def did_succeed(self):
        return self.success

    def scrape_info(self, soup):
        header = soup.find("div", {"id": "id_structure_header"})
        if not header:
            return {}
        site_info = self.parse_header(header)

        contact = soup.find("div", {"id": "id_contact_data"})
        site_info = self.add_contact_info(contact, site_info)

        address = soup.find("table", {"id": "id_structure_address"})
        site_info = self.add_address(address, site_info)

        return site_info

    def add_address(self, add_soup, info):
        add = add_soup.find_all("p")
        add = [a.getText() for a in add]
        info["address"] = " ".join(add[1:])
        return info

    def strip_space(self, text):
        return " ".join(text.split())

    def add_contact_info(self, contact_soup, info):
        host = contact_soup.find("h5").getText()
        info["host"] = host
        info["contact"] = []
        rest_info = contact_soup.find_all("p")
        for ctx in rest_info:
            info["contact"].append(" ".join(ctx.getText().split()))
        return info

    def parse_header(self, header_soup):
        situation = header_soup.getText().split("\n")[1].strip()
        name = header_soup.find("h1").getText()
        info = {"name": name, "activities": [], "situation": situation}
        activities = header_soup.find_all("div", {"class": "activity-type-button"})
        for activity in activities:
            act = activity.getText()
            info["activities"].append(act)

        return info


def format_row(index, result):
    row = [index]
    cols = ["name", "host", "activities", "situation", "contact", "address"]
    for col in cols:
        data = result[col]
        if type(data) == type([]):
            data = ", ".join(data)
        row.append(data)
    return row


if __name__ == "__main__":

    xl_helper = WriterHelper(1, XLWriter())
    xlsheet_header = [
        "Index",
        "Name",
        "Host",
        "Activities",
        "Situation",
        "Contact",
        "Address",
    ]
    xl_helper.init_xl(xlsheet_header)

    base_url = "https://www.accueil-paysan.com"
    scraper = Accueil(base_url)

    index = 1
    for num in range(2000):
        print(f"trying: {num}")
        try:
            data = scraper.request_page(
                "/fr/catalog/structure/{}/".format(num), scraper.scrape_info
            )
            if data != False:
                row = format_row(index, data)
                xl_helper.add_row(row)
                index += 1
        except KeyboardInterrupt:
            print("program killed.")
            exit(0)
        except:
            print(f"{num} failed.")
            continue

    xl_helper.save("accueil-paysan")

from bs4 import BeautifulSoup
from requests import get
import re
import urllib3
import urllib
import random
import time
import json


class Parser:
    def __init__(self):
        self.proxies = {"http": "203.189.142.23:53281"}  # , "https": "186.10.65.5:999"}
        self.user_agents = [
            # Chrome
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36",
            "Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",
            # Firefox
            "Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)",
            "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)",
            "Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko",
            "Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko",
            "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko",
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)",
            "Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko",
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)",
            "Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko",
            "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)",
            "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)",
            "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)",
        ]
        # self.url = "https://www.bing.com/search?q=%s"
        self.url = "https://www.google.com/search?rlz=1C1CHBF_enUS818US818&q=%s"
        self.all = []
        self.proxy_host = "104.43.244.233:" + "80"
        self.latest_result = {}
        self.max_tries = 3
        self.curr_try = 0
        self.open_files = []

    def make_request(self, query, current_location):
        # response = get(self.url + query, proxies=self.proxies)
        # https://www.bing.com/search?q=
        # "https://www.google.com/search?rlz=1C1CHBF_enUS818US818&q="
        address = self.url % urllib.parse.quote_plus(query)
        user_agent = self.get_random_user_agent()

        self.wait_random_time()
        print("requesting...")
        getRequest = urllib.request.Request(
            address, data=None, headers={"User-Agent": user_agent},
        )
        # getRequest.set_proxy(self.proxy_host, "http")
        f = urllib.request.urlopen(getRequest)
        htmlResult = f.read().decode("utf-8")
        self.search(htmlResult, current_location)

    def search(self, response, current_location):
        soup = BeautifulSoup(response, "html.parser")
        self.get_details(soup, current_location)

    def get_details(self, soup, current_location):
        print("crawling page...")
        try:
            if "bing" in self.url:
                module = soup.find("div", {"class": "b_sideBleed"})
                title = module.find("h2", {"class": "b_entityTitle"})
                address_phone = module.find_all("div", {"class": "b_factrow"})
                current_location["Title"] = title.getText()
                for item in address_phone:
                    info = item.getText().split(":")
                    current_location[info[0]] = info[1]

                self.latest_result = current_location

            elif "google" in self.url:
                # self.google_scraper1(soup, current_location)
                spans = soup.find_all("span")
                up_next = False
                # google has made it hard to find specific tags. instead crawl through ever span tag.
                for span in spans:
                    span_text = span.getText()

                    if up_next:
                        current_location["Address"] = span_text
                        up_next = False

                    elif "Address" in span_text:
                        up_next = True

                    elif "+33" in span_text:
                        current_location["Phone"] = span_text

                    # if both fields have been filled in with values then exit loop.
                    if (
                        current_location.get("Phone") != None
                        and current_location.get("Address") != None
                    ):
                        break

                if (
                    current_location.get("Phone", None) == None
                    and current_location.get("Address", None) == None
                ):
                    self.try_again(current_location)
                else:
                    self.curr_try = 0
                    self.latest_result = current_location
                    # print(current_location)

            else:
                print("Search not valid")

            print("done with current location...")

        except:
            self.try_again(current_location)

    def try_again(self, current_location):

        if self.curr_try == 2:
            self.curr_try += 1
            self.last_try(current_location)

        elif self.curr_try >= self.max_tries:
            print("Could not read info")
            current_location["Info"] = "N/A"
            self.curr_try = 0
            self.latest_result = current_location

        else:
            self.curr_try += 1
            self.process(current_location)

    def google_scraper2(self, soup, current_location):
        spans = soup.find_all("span")
        for span, index in enumerate(spans):
            if "Address" in span.getText():
                current_location["Address"] = spans[index + 1].getText()
            if "Phone" in span.getText():
                current_location["Phone"] = spans[index + 1].getText()
        if current_location.get("Phone", None) == None:
            current_location["Phone"] = "N/A"
        if current_location.get("Address", None) == None:
            current_location["Address"] = "N/A"
        self.latest_result = current_location

    def google_scraper1(self, soup, current_location):
        address = soup.find("div", {"data-attrid": "kc:/location/location:address"})
        phone = soup.find(
            "div", {"data-attrid": "kc:/collection/knowledge_panels/has_phone:phone"},
        )
        if address != None:
            current_location["Address"] = address.getText()
        else:
            current_location["Address"] = "N/A"

        if phone != None:
            current_location["Phone"] = phone.getText()
        else:
            current_location["Phone"] = "N/A"

    # wait random amount of time between 15 and 60 seconds
    def wait_random_time(self):
        random_seconds = random.randrange(30, 120)
        print("sleeping for: ", random_seconds, " seconds...")
        time.sleep(random_seconds)

    def process(self, current_location):
        loc_city = current_location["city"]
        loc_place = current_location["place"]
        query = f"{loc_city}+{loc_place}"
        self.make_request(query, current_location)

    def last_try(self, current_location):
        loc_name = current_location["name"]
        loc_place = current_location["place"]
        query = f"{loc_place}+{loc_name}"
        self.make_request(query, current_location)

    def get_random_user_agent(self):
        random_index = random.randrange(0, len(self.user_agents))
        return self.user_agents[random_index]

    def write_out(self, out_file):
        pretty_str = self.format_obj(self.latest_result)
        out_file.write(pretty_str)
        out_file.write("\n")

    def format_obj(self, curr_obj):
        out_str = ""
        for key, value in curr_obj.items():
            out_str += key + ": " + value + "\n"

        return out_str

    def write_to_file(self):
        with open("output.txt", "w") as f:
            for place in self.all:
                for key, value in place.items():
                    f.write(key + ": " + re.sub("[^A-Za-z0-9 ]+", "", value) + "\n")
                f.write("\n")

    def eject(self, index):
        last_pro_file = open("processed_index.txt", "w")
        last_pro_file.write(index)
        last_pro_file.close()
        for files in self.open_files:
            try:
                files.close()
            except:
                print("one or more files already_closed")
        exit(0)


def run_scraper():

    parser = Parser()

    last_pro_file = open("processed_index.txt", "r")
    last_processed_index = int(last_pro_file.read())
    last_pro_file.close()

    out_file = open("detailed_output.txt", "a", encoding="utf-8")

    with open("output.json", "r") as f_in:

        json_data = json.load(f_in)
        parser.open_files = [f_in, out_file]

        try:
            for index, curr_obj in json_data.items():

                if int(index) > last_processed_index:
                    parser.curr_try = 0
                    parser.process(curr_obj)
                    parser.write_out(out_file)

        except KeyboardInterrupt:
            print("Interrupted")
            last_completed = str(int(index) - 1)
            try:
                parser.eject(last_completed)
                sys.exit(0)
            except SystemExit:
                parser.eject(last_completed)
                os._exit(0)
        except Exception as err:
            print("main process rejection:")
            print(str(err))
            last_completed = str(int(index) - 1)
            parser.eject(last_completed)

    # parser.eject()


def output_json():
    index = 0
    full_json = {}
    with open("output.txt", "r") as f_in:
        current_obj = {}
        for line in f_in:
            if not line.strip():
                full_json[index] = current_obj
                index += 1
                current_obj = {}
            else:
                line = line.split(":")
                current_obj[line[0]] = line[1].strip().rstrip()

    with open("output.json", "w") as f_out:
        f_out.write(json.dumps(full_json))

    f_out.close()
    f_in.close()


if __name__ == "__main__":

    run_scraper()

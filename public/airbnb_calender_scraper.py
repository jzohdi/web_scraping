"""
Since initial load of AirBnB is not hydrated content,
need to load the site in webdriver and wait until the calender is
hydrated, which may take some time.
"""

# from bs4 import BeautifulSoup
from requests import get
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time
from ..helpers.base_scraper import BaseScraper

options = Options()
# options.headless = True

# DRIVER_PATH="C:\Users\jakez\Desktop\FOLDER\chromedriver"

class Scraper(BaseScraper):
    def __init__(self, base_url):
        super().__init__(base_url)
        self.url = base_url

    def run(self):
        browser = webdriver.Chrome(ChromeDriverManager().install())
        browser.get(self.url)
        print("sleeping...")
        time.sleep(10)
        print("done sleeping...")
        # delay = 3 # seconds
        # try:
        #     myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.ID, 'IdOfMyElement')))
        #     print("Page is ready!")
        # except TimeoutException:
        #     print("Loading took too much time!")
        javaScript = """
            const main = () => { 
                    const seenDates = new Set()
                    const invalid = []
                    function getDatesOnPage() {
                        const invalid_dates = document.querySelectorAll("[aria-disabled='true']")
                        for (date_tag of invalid_dates) {
                            const childEle = date_tag.firstChild;
                            const value = childEle.getAttribute("data-testid");
                            if (value && !seenDates.has(value)) {
                                invalid.push(value)   
                                seenDates.add(value)
                            }
                        }
                    }
                    function clickNextOnCalender() {
                        const buttons = document.querySelectorAll("button[aria-disabled='false']")
                        if (buttons.length > 1) {
                            buttons[1].click();
                        } else {
                            buttons[0].click();
                        }
                    }
                    function datesAndNext() {
                        getDatesOnPage();
                        clickNextOnCalender();
                    }
                    datesAndNext();
                    invalid.push("break");
                    datesAndNext();
                    invalid.push("break");
                    datesAndNext();
                    invalid.push("break");
                    return invalid
            }

            return main()
        """
        result = browser.execute_script(javaScript)
        print(result)      
        return result  
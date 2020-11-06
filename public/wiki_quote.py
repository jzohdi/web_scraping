# -*- coding: utf-8 -*-
"""
Created on Mon Mar 18 16:24:47 2019

@author: jzohdi

this is meant to query the wiki quote random url and scrape all quotes from
that page.

to start call .run()
returns [...quote]

"""

from bs4 import BeautifulSoup
from requests import get
from random import shuffle
import threading, time, signal
from datetime import timedelta
from ..helpers.base_scraper import BaseScraper

class Scraper(BaseScraper):
    def __init__(self, base_url):
        super().__init__(base_url)
        self.url = base_url
        self.title = None
        self.status = None
        self.all_quotes = []    

    def parse_soup(self, soup):
        self.title = ' '.join(soup.find('title').get_text().split('-')[:-1])
        self.get_quotes_and_author(soup)
    
    def get_quotes_and_author(self, soup):
        if self.status != 200:
            return None
        quotes = soup.find_all('ul')
        shuffle(quotes)
        for quote in quotes:
            self.add_quote_if_valid(quote)
            
    def add_quote_if_valid(self, quote):
        this_quote = quote.find('li')
        this_author = quote.find('ul')
        if this_quote and this_author:
            ( this_quote, this_author ) = ( this_quote.get_text(), this_author.get_text() )
            ( this_quote, this_author ) = self.scrub_title_and_author(this_quote, this_author)
            if len(this_quote) > 10 and len(this_author) > 0:
                
                quote_dict = {'source': self.title.strip(), 
                              'author' : this_author.strip(), 
                              'quote' : this_quote.strip().replace('  ', ' ')}
                
                self.all_quotes.append(quote_dict)
        
        return self.all_quotes
            
    def scrub_title_and_author(self, text, author):
        title_to_list = self.title.split(" ")
        author_to_list = author.split(" ")
        for word in author_to_list:
            word = self.remove_end_quotes(word)
            text = text.replace(word, '')
        for word in title_to_list:
            text = text.replace(word, '')
        return ( text, author )
    
    def remove_end_quotes(self, word):
        if word.startswith("'") or word.startswith('"'):
            word = word[1:]
        if word.endswith('"') or word.endswith("'"):
            word = word[:-1]
        return word    
    

""" 
    Job class used to run multiple threads at once.
"""
DAY_TO_SECONDS = 86400
WAIT_TIME_SECONDS = 60

class ProgramKilled(Exception):
    pass
    
def signal_handler(signum, frame):
    raise ProgramKilled
    
class Job(threading.Thread):
    def __init__(self, interval, execute, *args, **kwargs):
        threading.Thread.__init__(self)
        self.daemon = False
        self.stopped = threading.Event()
        self.interval = interval
        self.execute = execute
        self.args = args
        self.kwargs = kwargs
        
    def stop(self):
                self.stopped.set()
                self.join()
    def run(self):
            while not self.stopped.wait(self.interval.total_seconds()):
                self.execute(*self.args, **self.kwargs)

"""
    parser = Parser()
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)
    job = Job(interval=timedelta(seconds=WAIT_TIME_SECONDS), execute=parser.make_request)
    job.start()

    while True:
          try:
              time.sleep(1)
              print('here')
          except (ProgramKilled,KeyboardInterrupt, SystemExit):
              print("Program killed: running cleanup code")
              job.stop()
              break

"""
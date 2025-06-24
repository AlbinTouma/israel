from core import Database, Logger, WebPage, Scraper
from datetime import datetime, date
import time
from random import randint
from selenium import webdriver
from selenium.webdriver.common.by import By
from core.scraper import Scraper
import re
from core.logger import Logger
from .homepage import HomePage
from .liveblog import LiveBlog
from .news import News
from .program_news import ProgramNews



class AljazeeraScraper():
    def __init__(self, skip_titles, driver):
        self.skip_titles = skip_titles
        self.driver  = driver

    def collect_titles(self):
        x = WebPage(website='aljazeera', link="https://www.aljazeera.com/tag/israel-palestine-conflict/")
        scraper = HomePage(x, 'aljazeera_links')
        scraper.run()
        print("DONE")

    def full_run(self):

        file = 'aljazeera_data'
        js = Database.read_jsonl(filename='aljazeera_links')
        if self.skip_titles == "Yes":
            self.collect_titles()

        js = js[586:]
        
        count = 0
        for i in js:
            page = WebPage(link=i['link'])
            opts = {
                "news": News(page, file, self.driver) , 
                "news/liveblog": LiveBlog(page, file, self.driver),
                "program/newsfeed": ProgramNews(page, file, self.driver)
            }

            for key, scraper in opts.items():
                if i['media_type'] == key:
                    scraper.run()
                    count += 1
                    time.sleep(randint(1, 3))

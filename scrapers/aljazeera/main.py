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

    @staticmethod
    def collect_titles():
        x = WebPage(website='aljazeera', link="https://www.aljazeera.com/tag/israel-palestine-conflict/")
        scraper = HomePage(x, 'aljazeera_links')
        scraper.run()
        print("DONE")

    @staticmethod
    def full_run(skip_titles: str):

        file = 'aljazeera_data'

        js = Database.read_jsonl(filename='aljazeera_links')
        if skip_titles == "Yes":
            AljazeeraScraper.collect_titles()
        
        count = 0
        for i in js:
            page = WebPage(link=i['link'])
            opts = {
                "news": News(page, file) , 
                "news/liveblog": LiveBlog(page, file),
                "program/newsfeed": ProgramNews(page, file)
            }

            for key, scraper in opts.items():
                if i['media_type'] == key:
                    scraper = scraper
                    scraper.run()
                    count += 1
                    time.sleep(randint(1, 3))

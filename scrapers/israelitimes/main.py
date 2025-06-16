from core import Database, Logger, WebPage, Scraper
from datetime import datetime, date
import time
from random import randint
from selenium import webdriver
from selenium.webdriver.common.by import By
from core.scraper import Scraper
import re
from core.logger import Logger
from core.scroll import ScrollBehaviour
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from core.database import Database
from .homepage import HomePage
from .scrape_article import ScrapeArticle
from .liveblog import LiveBlog
from .blogs import Blog


class IsraeliTimes:

    @staticmethod
    def collect_titles():
        x = WebPage(website='israelitimes', link="https://www.timesofisrael.com/")
        scraper = HomePage(x, 'test')
        scraper.run()
        print("DONE")

    @staticmethod
    def full_run(skip_titles: str):


        file = 'test_data'
        if skip_titles == 'Yes':
            IsraeliTimes.collect_titles()
        
        js = Database.read_jsonl(filename='israelitimes_links')
        count = 0
        for i in js:
            page = WebPage(link=i['link'])
            opts = {
                "article": ScrapeArticle(page, file) , 
                "liveblog": LiveBlog(page, file),
                "blog": Blog(page, file)
            }

            for key, scraper in opts.items():
                if i['media_type'] == key:
                    scraper = scraper
                    scraper.run()
                    count += 1
                    time.sleep(randint(1, 3))

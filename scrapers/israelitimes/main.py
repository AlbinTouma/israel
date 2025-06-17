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
    def __init__(self, skip_titles, driver):
        self.skip_titles = skip_titles
        self.driver = driver

    def collect_titles(self):
        x = WebPage(website='israelitimes', link="https://www.timesofisrael.com/")
        scraper = HomePage(x, 'test', self.driver)
        scraper.run()
        print("DONE")

    def collect_blog(self):
        x = Blog(WebPage(link="https://blogs.timesofisrael.com/oct-7-dawn-french-and-the-dark-arts-of-amnesia-and-illusion/"), 'test', self.driver)
        x.run()

    def full_run(self):


        file = 'test_data'
        if self.skip_titles == 'Yes':
            IsraeliTimes.collect_titles(self)
        
        js = Database.read_jsonl(filename='israelitimes_links')
        count = 0
        opts = None
        for i in js:
            page = WebPage(link=i['link'])
            opts = {
                "article": ScrapeArticle(page, file, self.driver) , 
                "liveblog": LiveBlog(page, file, self.driver),
                "blog": Blog(page, file, self.driver)
            }
            for key, scraper in opts.items():
                if i['media_type'] == key:
                    scraper.run()
                    count += 1
                    time.sleep(randint(1, 3))

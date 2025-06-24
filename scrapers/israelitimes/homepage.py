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



class HomePage(Scraper):

    def detect_type_article(self,link: str) -> str:
        """Categorises articles for israelitimes."""
        mappings = {
                'liveblog': 'liveblog',
                'https://blogs.timesofisrael.com/': 'blog',
                'https://jewishchronicle.timesofisrael.com/': 'jewishchronicle',
                'https://njjewishnews.timesofisrael.com/': 'new_jersey_news',
                'https://www.timesofisrael.com/': 'article'
        }

        for key, value in mappings.items():
            if key in link:
                return value



    def scrape_method(self):
        result = []
        unique_elements = set()
        time.sleep(3)
        while True:
            scroll = ScrollBehaviour.scroll_full_page(self.driver)
            if not scroll:
                break

            a_elements = self.driver.find_elements(By.XPATH, '//div[@class="headline"]/a')

            new_list = []
            for a in a_elements:
                href = a.get_attribute('href')
                if href in unique_elements:
                    continue
                unique_elements.add(href)
                new_list.append((a, href))

            for a, href in new_list:
                type_of_article = self.detect_type_article(href)
                w =  WebPage(
                #    unique_id=unique_id,
                    website='timesofisrael',
                    link=href,
                    date=None,
                    media_type=type_of_article,
                    content=None)

                result.append(w)

            if len(result) > 10:
                Database.write_to_jsonl(result, filename='israelitimes_links')
                result = []
            
        print('Collecting:', len(result), 'articles self.driver the page')
 

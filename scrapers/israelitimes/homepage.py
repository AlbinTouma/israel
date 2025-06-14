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
                'https://jewishchronicle.timesofisrael.com/': 'jewishchronicle'
        }

        for key, value in mappings.items():
            if key in link:
                return value

        return 'article'


    def scrape_method(self):
        result = []
        unique_elements = set()
        while True:
            scroll = ScrollBehaviour.scroll_full_page(self.driver)
            if not scroll:
                break

            a_elements = self.driver.find_elements(By.XPATH, '//div[@class="headline"]/a')

            new_list = []
            for a in a_elements:
                title = a.text
                unique_id = Database.generate_unique_id(title, self.driver.current_url)

                if unique_id in unique_elements:
                    continue
                unique_elements.add(unique_id)
                new_list.append((a, unique_id, title))

            for a, unique_id, title in new_list:
                href = a.get_attribute("href")
                type_of_article = self.detect_type_article(href)

                w =  WebPage(
                    unique_id=unique_id,
                    title=title,
                    website='timesofisrael',
                    url=self.driver.current_url,
                    link=href,
                    date=None,
                    media_type=type_of_article,
                    content=None)

                result.append(w)

            if len(result) > 10:
                Database.write_to_jsonl(result, filename='israelitimes_links')
            
        print('Collecting:', len(result), 'articles self.driver the page')
 

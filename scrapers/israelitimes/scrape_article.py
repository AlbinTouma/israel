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

class ScrapeArticle(Scraper):

    def scrape_method(self):
        """Scrapes title, content, date from the article page."""
        result = []
        unique = set()
        
        while True:
            
            scroll = ScrollBehaviour.scroll_full_page(self.driver)
            if not scroll:
                break

            new_list = []
            try:
                title = self.driver.find_element(By.XPATH, '//h1[@class="headline"]').text
                unique_id = Database.generate_unique_id(title, self.driver.current_url)
                content = self.driver.find_element(By.XPATH, '//div[@class="the-content"]').text
                date = self.driver.find_element(By.XPATH, '//span[@class="date"]').text
                if unique_id in unique:
                    continue
                unique.add(unique_id)
                new_list.append((unique_id, title, content, date))
            except Exception as e:
                print(f"{e}")

            for unique_id, title, content, date in new_list:

                article = WebPage(
                    unique_id=unique_id,
                    website='timesofisrael',
                    url=self.driver.current_url,
                    title =title,
                    date=date,
                    media_type='article',
                    content=content
                )

                result.append(article)

            print(result)
            Database.write_to_jsonl(result, 'israelitimes_data')



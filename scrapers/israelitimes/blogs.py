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
from core.scroll import ScrollBehaviour


class Blog(Scraper):

    def scrape_method(self):
        """
        Scrapes title, content, date from the blog page. Scrolling to the bottom opens new blog post. 
        The First blog post should be visible in the dom so no need to scroll.
        """
        result = []
        try:
            title = self.driver.find_element(By.XPATH, '//h1[@class="headline"]').text
            unique_id = Database.generate_unique_id(title, self.driver.current_url)
            content = self.driver.find_element(By.XPATH, '//div[@class="article-content"]').text
            date = self.driver.find_element(By.XPATH, '//aside[@class="block cols1"]//div[@class="date"]').text

            result.append(WebPage(
                unique_id=unique_id,
                website='timesofisrael',
                title =title,
                date=date,
                link=None,
                media_type="blog",
                content=content
            ))
            
        except Exception as e:
            print(e)

        print(result)
        Database.write_to_jsonl(result, 'israelitimes_data')



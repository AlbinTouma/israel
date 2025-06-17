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


class News(Scraper):

    def scrape_method(self):
        ScrollBehaviour.close_cookie_banner(self.driver)
        result = []

        while True:

            scroll = ScrollBehaviour.scroll_full_page(self.driver)
            if not scroll:
                break


            try:
                h = self.driver.find_elements(By.XPATH, '//main//div[@aria-live="polite"]//p')
                title = self.driver.find_element(By.XPATH, '//header//h1').text
                unique_id = Database.generate_unique_id(title, self.driver.current_url)
                date_simple = self.driver.find_element(By.XPATH, '//div[@class="date-simple"]//span[@aria-hidden]').text

                strings = []
                for i in h:
                    strings.append(i.text)
                    
                content = ''.join(strings)

                result.append(WebPage(unique_id = unique_id, website='aljazeera', url=self.driver.current_url, media_type='news', date=date_simple, title=title, content=content))

                print(result)
            except Exception as e:
                print('EXCEPTION')

        print(result)
        Database.write_to_jsonl(result, filename='aljazeera_data')



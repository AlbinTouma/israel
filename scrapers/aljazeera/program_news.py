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




class ProgramNews(Scraper):

    def scrape_method(self):
        print("SCRAPING")
        ScrollBehaviour.close_cookie_banner(self.driver)
        result = []

        while True:
            scroll = ScrollBehaviour.scroll_full_page(self.driver)


            try:
                title = self.driver.find_element(By.XPATH, '//main//h1').text
                unique_id = Database.generate_unique_id(title,self.driver.current_url)


                date_simple = self.driver.find_element(By.XPATH, '//*[@id="main-content-area"]/div[2]/div[2]/div[1]/div/div/span[2]').text
                p = self.driver.find_elements(By.XPATH, '//*[@id="main-content-area"]/div[2]/p')
                strings = []
                for i in p:
                    strings.append(i.text)
                content = ''.join(strings)

                result.append(WebPage(unique_id=unique_id, website='aljazeera', url=self.driver.current_url, media_type='program/newsfeed', date=date_simple, title=title, content=content))
            except Exception as e:
                print(e)
            
            if not scroll:
                break
        print(result)
        Database.write_to_jsonl(result, filename='aljazeera_data')



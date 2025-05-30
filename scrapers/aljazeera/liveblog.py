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

class LiveBlog(Scraper):


    def scrape_method(self):
        ScrollBehaviour.close_cookie_banner(self.driver)
        time.sleep(1)



        while True:
            try:
                loading = self.driver.find_element(By.XPATH,'//div[@class="live-blog--loading"]')
                if loading.is_displayed():
                    ScrollBehaviour.scroll_into_view(self.driver,loading)

            except NoSuchElementException: 
                print("Reached end of liveblog. Scraping completed.")
                break

            feed_list = self.driver.find_element(By.XPATH,'//ul[@class="feed-list"]') 
            feed_item = feed_list.find_elements(By.XPATH, './/li')
            print(len(feed_item))

            for i in feed_item:
                try:
                    title = i.find_element(By.XPATH,'.//h2')
                    print("TITLE IS", title.text)
                except Exception:
                    continue
            # content_blocks = i.find_elements(By.XPATH,'//div[contains(@class, "wysiwyg") and contains(@class, "wysiwyg--all-content")]')


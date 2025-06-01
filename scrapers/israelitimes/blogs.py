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



class Blogs(Scraper):
    def collect_blogs(self, driver, scrape_object: WebPage) -> WebPage:
        """Scrapes title, content, date from the blog page."""
        try:
            title = driver.find_element(By.XPATH, '//h1[@class="headline"]').text
            content = driver.find_element(By.XPATH, '//div[@class="article-content"]').text
            date = driver.find_element(By.XPATH, '//aside[@class="block cols1"]//div[@class="date"]').text
            article = WebPage(
                website='timesofisrael',
                title =title,
                date=date,
                link=scrape_object.link,
                media_type=scrape_object.media_type,
                content=content
            )  
            return article
            
        except Exception as e:
            return f"'Error': {e}, 'title', {scrape_object.title}, 'link', {scrape_object.link} \n"



 

from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import json
import undetected_chromedriver as uc
import time
from random import randint
from datetime import datetime, date
from .models import WebPage
from .database import Database
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from abc import ABC, abstractmethod
   
class Scraper(ABC):
    def __init__(self, scrape_object: WebPage, filename: str, driver=None):
        self.scrape_object = scrape_object
        self.filename = filename
        self.driver = driver

    def safe_get_text(self, element, xpath):
        try:
            return element.find_element(By.XPATH, xpath).text
        except Exception:
            return None

    def safe_get_elements(self, element, xpath):
        try:
            return element.find_elements(By.XPATH, xpath)
        except Exception:
            return []


    @abstractmethod
    def scrape_method(self):
        pass

    def run(self):
        self.driver.get(self.scrape_object.link)
        self.scrape_method()

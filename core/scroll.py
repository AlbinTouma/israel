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

class ScrollBehaviour:
    
    def close_cookie_banner(driver):
        driver.execute_script("""
            var banner = document.getElementById('onetrust-group-container');
            var overlay = document.getElementById('onetrust-consent-sdk');
            if (banner) banner.style.display = 'none';
            if (overlay) overlay.style.display = 'none';
        """)

    def scroll_full_page(driver):
            old_height = driver.execute_script("return document.body.scrollHeight")
            driver.execute_script("""
                window.scrollBy({
                    top: document.body.scrollHeight - window.scrollY,
                    left: 0,
                    behavior: 'smooth'
                });
                            
            """)
            
            time.sleep(3)
            new_height = driver.execute_script("return document.body.scrollHeight")
            return new_height != old_height

    def scroll_into_view(driver, element):
        try:
            driver.execute_script("""arguments[0].scrollIntoView({
                                  behavior: 'smooth',
                                  block: 'center'
                                  });""", element)
        except Exception as e:
            print(f"REACHED END OF INFINITY PAGE \n {e}")

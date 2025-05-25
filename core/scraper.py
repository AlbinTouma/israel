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

class Browser:
    def __init__(self, scraper):
        self.Scraper = scraper
    
    def close_cookie_banner(self):
        self.Scraper.driver.execute_script("""
            var banner = document.getElementById('onetrust-group-container');
            var overlay = document.getElementById('onetrust-consent-sdk');
            if (banner) banner.style.display = 'none';
            if (overlay) overlay.style.display = 'none';
        """)
    
    def click_button(self):
        try:
            button = self.Scraper.driver.find_element(By.XPATH, '//button[@data-testid="show-more-button" and contains(@class, "show-more-button") and contains(@class, "big-margin")]')        
        except Exception as e:
            return False
            
        if button.is_displayed() and button.is_enabled():
            self.Scraper.driver.execute_script("arguments[0].click();", button)
            time.sleep(1)
            return True
        return False

    
    def scroll_method(self) -> bool:
        '''Returns True if button is clicked or new height is not the same as old height'''
        try:
            self.close_cookie_banner()
            old_height = self.Scraper.driver.execute_script("return document.body.scrollHeight")
            button_clicked: bool = self.click_button()
            # Smooth scroll to bottom (not jumping)
            self.Scraper.driver.execute_script("""
                window.scrollBy({
                    top: document.body.scrollHeight - window.scrollY,
                    left: 0,
                    behavior: 'smooth'
                });
            """)


            time.sleep(1)
            new_height = self.Scraper.driver.execute_script("return document.body.scrollHeight")
            return new_height != old_height or button_clicked
        except Exception as e:
            print("ERROR IN SCROLL:", e)




class Scraper:
    def __init__(self, scrape_object: WebPage, scraper_function, filename: str):
        self.scrape_object = scrape_object
        self.scraper_function = scraper_function
        self.filename = filename

    def run(self):
        # This function is used to run the scraper
        self.driver  = uc.Chrome(headless=False,use_subprocess=False)
        self.driver.get(self.scrape_object.link)
        browser = Browser(self)
        consecutive_change = 0
        seen_links = set()

        while True:
            result: list[WebPage] | Exception 
            stop_flag: bool 
        
            result, stop_flag = self.scraper_function(self.driver, self.scrape_object)
            
            if isinstance(result, Exception):
                print(f"Exception, skipping {self.scrape_object.title}")
                break
            
            if result:
                deduped_list = []
                for page in result:
                    if page.link not in seen_links:
                        deduped_list.append(page)
                        seen_links.add(page.link)
                               
                Database.write_to_jsonl(deduped_list, self.filename)

            if stop_flag:
                break
            
            content_change: bool = browser.scroll_method()

            if not content_change:
                consecutive_change += 1
                if consecutive_change >= 3:
                    print('No new content upon scroll')
                    break

        self.driver.quit()

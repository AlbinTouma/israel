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


class Browser:
    def __init__(self, scraper):
        self.Scraper = scraper
    
    def click_button(self):
        button = self.Scraper.driver.find_element(By.XPATH, '//button[@class="show-more-button big-margin"]')
        if button.is_displayed():
            button.click()
            time.sleep(1)
            return True
        return False
    
    def scroll_method(self) -> bool:
        '''Returns True if button is clicked or new height is not the same as old height'''
        try:
            old_height = self.Scraper.driver.execute_script("return document.body.scrollHeight")
            self.Scraper.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
            button_clicked: bool = self.click_button()
            new_height = self.Scraper.driver.execute_script("return document.body.scrollHeight")
            return new_height != old_height or button_clicked
        except Exception as e:
            print("Error:", e)



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
            content_change: bool = browser.scroll_method()
            result, stop_flag = self.scraper_function(self.driver, self.scrape_object)

            if result:
                deduped_list = []
                for page in result:
                    if page.link not in seen_links:
                        deduped_list.append(page)
                        seen_links.add(page.link)
                               
                Database.write_to_jsonl(deduped_list, self.filename)

            if stop_flag:
                break
            
            if not content_change:
                consecutive_change += 1
                if consecutive_change >= 3:
                    print('No new content upon scroll')
                    break

        self.driver.quit()

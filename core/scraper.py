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


class Scraper:
    def click_show_more_button(self, driver) -> bool:
        try:
            button = driver.find_element(By.XPATH, '//button[@class="show-more-button big-margin"]')
            if button.is_displayed():
                button.click()
                time.sleep(1)
                return True
        
        except Exception as e:
            pass
        return False
            
    def scroll_method(self, driver, scraper_function=None, scrape_object=None, filename=None):
        try:
            last_height = driver.execute_script("return document.body.scrollHeight")
            same_height_count = 0
            button_pressed_count = 0
            seen_links = set()

            while True:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(1)

                button_clicked = self.click_show_more_button(driver)
                if button_clicked:
                    button_pressed_count += 1

                if scraper_function and scrape_object:
                    result, stop_flag = scraper_function(driver, scrape_object, seen_links)
                    print(filename)
                    Database.write_to_jsonl(result, filename)
                    if stop_flag:
                        print("Criteria met, terminating infinity scroll.")
                        break

    
                new_height = driver.execute_script("return document.body.scrollHeight")
            
                if new_height == last_height:
                    same_height_count += 1
                    if same_height_count >= 3:
                       # logger.info("Reached the end of the page.")
                        break
                else:
                    same_height_count = 0
                    last_height = new_height
                    

        except Exception as e:
            print("Error:", e)

        

    def run(self, scrape_object: WebPage, scraper_function, filename: str, incremental: bool):
        # This function is used to run the scraper
        self.driver  = uc.Chrome(headless=False,use_subprocess=False)
        self.driver.get(scrape_object.link)

        if incremental:
            self.scroll_method(
                driver=self.driver,
                scraper_function=scraper_function,
                scrape_object=scrape_object,
                filename=filename
            )

        else:
            self.scroll_method(driver=self.driver)
            result =  scraper_function(self.driver, scrape_object)
            Database.write_to_jsonl(result, filename)
        
        self.driver.quit()

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

class HomePage(Scraper):


    def convert_date(self, date_str: str) -> datetime.date:
        for fmt in ("%d %B %Y", "%d %b %Y"):  # Try full and short month names
            try:
                return datetime.strptime(date_str, fmt).date()
            except ValueError:
                continue
        raise ValueError(f"Date format not recognized: {date_str}")
    
    def identify_media_type(self, link: str) -> str:
        link = link.removeprefix('https://www.aljazeera.com/')
        match = re.search('(.*?)(?=/\d{4}/\d{1,2}/\d{1,2}/)',link)
        if match:
            return match.group(1)
        else:
            return None
    
    def scrape_method(self):
        scroll_number = 0
        ScrollBehaviour.close_cookie_banner(self.driver)
        unique_set =  set()
        result = []
        while True:
            try:
                button = self.driver.find_element(By.XPATH, '//button[@data-testid="show-more-button" and contains(@class, "show-more-button") and contains(@class, "big-margin")]')        
                if button.is_displayed() and button.is_enabled():
                    ScrollBehaviour.scroll_into_view(self.driver,button)
                    self.driver.execute_script("arguments[0].click();", button)
                    scroll_number += 1
                    print("Scroll number", scroll_number)
                    time.sleep(2)
                    
            except NoSuchElementException: 
                break

            news_feed = self.driver.find_elements(By.XPATH, '//section[@aria-label="Content Feed"]//article') 
            new_list = []
            for article in news_feed:
                title = article.find_element(By.XPATH,'.//h3[@class="gc__title"]').text
                unique_id = Database.generate_unique_id(title, self.driver.current_url)
                if unique_id in unique_set:
                    continue
                unique_set.add(unique_id)
                new_list.append((article, unique_id, title))


            for article, unique_id, title in new_list:
                href = article.find_element(By.XPATH, './/a[@class="u-clickable-card__link"]')
                href = href.get_attribute('href')
                date_span = article.find_element(By.XPATH,'.//div[@class="date-simple"]//span[@aria-hidden="true"]').text.strip()
                result_date = self.convert_date(date_span)
                media_type = self.identify_media_type(href)
                
                print(f"ID: {unique_id},\n title {title} \n, HREF: {href},\n DATE: {date_span},/n MEDIA: {media_type}\n\n")
                result.append(WebPage(
                        website='aljazeera',
                        url=self.driver.current_url,
                        date=result_date,
                        title=title,
                        link=href,
                        media_type=media_type
                    ))

            if result_date < date(2024, 10, 5):
                print(True)
            else:
                print(date, result_date, False)


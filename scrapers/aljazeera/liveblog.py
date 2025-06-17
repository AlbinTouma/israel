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


class LiveBlog(Scraper):


    def scrape_method(self):
        """
        Creates a unique id based of title and current.url and then scrapes
        cards after scroll. 

        IMPORTANT CAVEAT! 

        There are sometimes two cards with the same title, ie "editor's choice"
        or "you're joining us".
        
        Only one is saved despite content being different.

        This is why lenght of results differs from number of li found on page.'
        """
        ScrollBehaviour.close_cookie_banner(self.driver)
        result = []
        broken_li = 0
        exception_count = 0
        seen_ids = set()
        scroll_number = 0

        while True:
            try:
                loading = self.driver.find_element(By.XPATH,'//div[@class="live-blog--loading"]')
                if loading.is_displayed():
                    ScrollBehaviour.scroll_into_view(self.driver,loading)
                    scroll_number += 1
                    time.sleep(2)
                    
            except NoSuchElementException: 
                break

            feed_list = self.driver.find_element(By.XPATH, '//ul[@class="feed-list"]')
            feed_items = feed_list.find_elements(By.XPATH, './/li')

            print(f"Scroll {scroll_number}, Found {len(feed_items)} total <li>")
            
            new_items = []
            for li in feed_items:
                try:
                    title_element = li.find_element(By.XPATH, './/h2').text
                    unique_id = Database.generate_unique_id(title_element, self.driver.current_url)

                    if unique_id in seen_ids:
                        continue

                    seen_ids.add(unique_id)

                    new_items.append((li, unique_id, title_element))

                except Exception as e:
                    broken_li += 1
                    continue # skip broken li


            print(f"Scroll: {scroll_number}, New items this round: {len(new_items)}")

            
            for i, unique_id, title  in new_items:
                try:
                    date = i.find_element(By.XPATH,'.//div[@class="date-relative"]').text
                    content_blocks = i.find_elements(By.XPATH,'.//div[contains(@class, "wysiwyg") and contains(@class, "wysiwyg--all-content")]')
                    content = ''.join([p.text for p in content_blocks])
                    w = WebPage(
                           unique_id=unique_id, 
                           title=title,
                           url=self.driver.current_url, 
                           content=content, 
                           date=date,
                           media_type='news/liveblog'
                           )
                    
                    result.append(w)

                except Exception as e:
                    exception_count += 1
                    print(f"FAIL: {title} - {e}")

        print('Items scraped', len(result))
        print('Broken li', broken_li)
        print('Exceptions', exception_count)
        for i in result:
            Database.write_to_jsonl(i, 'aljazeera_data')
            print(i.unique_id, i.title)



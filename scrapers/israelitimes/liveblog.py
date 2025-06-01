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

    def convert_timestamp_epoch(self, data_timestamp):
        if data_timestamp:
            try:
                timestamp = int(data_timestamp)
                dt_object = datetime.utcfromtimestamp(timestamp)
                epoch = dt_object.strftime('%Y-%m-%d %H:%M:%S')
                return epoch
            except ValueError:
                return None

        return None


    def scrape_method(self):
        """Scrapes title, content, date from the liveblog page."""
        result = []
        unique_set = set()
        index_div = 1
        l = 0
        while True:
            divs = self.driver.find_elements(By.XPATH, '//div[@class="the-content"]//div[@data-item]')
            l = len(divs)

            ScrollBehaviour.scroll_into_view(self.driver, divs[index_div])
            index_div += 5

            if index_div >= l:
                break

            new_list  = []
            for div in divs:
                try:
                    title = div.find_element(By.XPATH, './/div[@class="liveblog-paragraph"]//h4').text
                except Exception as e:
                    continue

                unique_id = Database.generate_unique_id(title, self.driver.current_url)

                if unique_id in unique_set:
                    continue
                unique_set.add(unique_id)
                new_list.append((div, unique_id, title))

            for div, unique_id, title in new_list:
                try:
                    content = div.find_elements(By.XPATH, './/div[@class="liveblog-paragraph"]//p')
                    content = ''.join([i.text for i in content])
                    href = div.find_element(By.XPATH, './/div[@class="liveblog-paragraph"]//h4//a')
                    href = href.get_attribute('href')
                    data_time_span = div.find_element(By.XPATH, './/div[@class="liveblog-date"]//span')
                    data_timestamp = data_time_span.get_attribute('data-timestamp')
                    epoch = self.convert_timestamp_epoch(data_timestamp)

                    result.append(WebPage(
                        unique_id=unique_id,
                        website='timesofisrael',
                        url=self.driver.current_url,
                        title =title,
                        date=epoch,
                        link=href,
                        media_type='liveblog',
                        content=content
                    ))

                    
                except Exception as e:
                    print(f'Error at {title} -> {e}')

        if len(result) > 10:
            Database.write_to_jsonl(result, 'test')
            result = []

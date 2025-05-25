from core import Database, Logger, WebPage, Scraper
from datetime import datetime, date
import time
from random import randint
from selenium import webdriver
from selenium.webdriver.common.by import By
from core.scraper import Scraper
import re

class AljazeeraScraper():

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
    

    def collect_page_titles(self, driver, _: WebPage) -> tuple[list[WebPage], bool]:
        try:
            result_date = None
            titles = driver.find_elements(By.XPATH, '//h3[@class="gc__title"]')
            hrefs = driver.find_elements(By.XPATH, '//a[@class="u-clickable-card__link"]')
            dates = driver.find_elements(By.XPATH, '//div[@class="date-simple"]//span[@aria-hidden="true"]')

            result = []
            for title, link, article_date in zip(titles, hrefs, dates):
                href = link.get_attribute('href')
                media_type = self.identify_media_type(href)
                result_date = self.convert_date(article_date.text)
                           
                result.append(WebPage(
                        website='aljazeera',
                        url=driver.current_url,
                        date=article_date.text,
                        title=title.text,
                        link=href,
                        media_type=media_type
                    ))

            if result_date < date(2024, 10, 5):
                return result, True

            return result, False
        

        except Exception as e:
            print("Exception:", e)
            return [], False
        
    def collect_newspage(self, driver, _: WebPage) -> tuple[list[WebPage], bool]:
        h = driver.find_elements(By.XPATH, '//main//div[@aria-live="polite"]//p')
        title = driver.find_element(By.XPATH, '//header//h1').text
        date_simple = driver.find_element(By.XPATH, '//div[@class="date-simple"]//span[@aria-hidden]').text

        strings = []
        for i in h:
            strings.append(i.text)
            
        content = ''.join(strings)

        result = []
        result.append(WebPage(website='aljazeera', url=driver.current_url, media_type='news', date=date_simple, title=title, content=content))
        
        return result, None
    

    def collect_newsfeed(self, driver, _: WebPage) -> tuple[list[WebPage], bool]:
        title = driver.find_element('').text
        date_simple = driver.find_element().text
        p = driver.find_elements()
        strings = []
        for i in p:
            strings.append(i.text)

        content = ''.join(strings)
        result = []
        result.append(WebPage(website='aljazeera', url=driver.current_url, media_type='newsfeed', date=date_simple, title=title, content=content))



    def run_collect_page_titles(self):
        homepage = WebPage(link='https://www.aljazeera.com/tag/israel-palestine-conflict/', media_type='homepage')
        Scraper(scrape_object=homepage, scraper_function=self.collect_page_titles, filename='aljazeera_links').run()
        time.sleep(randint(1, 3))

   
    def run_collect_newspage(self):
        dict_list = Database.read_jsonl_to_df(filename='aljazeera_links')
        for d in dict_list:
            if '/news/' in d['link']:
                page = WebPage(link=d['link'], media_type='news')
                Scraper(scrape_object=page, scraper_function=self.collect_newspage, filename='aljazeera').run()
                time.sleep(randint(1,3))


    def run(self):
        self.run_collect_page_titles()
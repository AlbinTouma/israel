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





class IsraeliTimesScraper():
    def __init__(self):
        self.scraper = Scraper()

    def scrape_article(self, driver, scrape_object: WebPage) -> WebPage:
        """Scrapes title, content, date from the article page."""
        try:
            title = driver.find_element(By.XPATH, '//h1[@class="headline"]').text
            content = driver.find_element(By.XPATH, '//div[@class="the-content"]').text
            date = driver.find_element(By.XPATH, '//span[@class="date"]').text
            article = WebPage(
                website='timesofisrael',
                title =title,
                date=date,
                link=scrape_object.link,
                media_type=scrape_object.media_type,
                content=content
            )

            if "Today" in article.date:
                new_date = datetime.date.today().strftime("%Y-%m-%d")
                article.date = new_date

            return article
        
        except Exception as e:
            return f"'Error': {e}, 'title', {scrape_object.title}, 'link', {scrape_object.link} \n"


    def collect_liveblog(self, driver, scrape_object: WebPage) -> list[WebPage]:
        """Scrapes title, content, date from the liveblog page."""
        try:
            title = driver.find_elements(By.XPATH, '//div[@class="liveblog-paragraph"]//h4')
            content = driver.find_elements(By.XPATH, '//div[@class="liveblog-paragraph"]//p')
            href = driver.find_elements(By.XPATH, '//div[@class="liveblog-paragraph"]//h4//a')
            dates = driver.find_elements(By.XPATH, '//div[@class="liveblog-date"]//a//span')
            result = []
            print(
                "title:", len(title), 
                "content:", len(content), 
                "link:", len(href), 
                "date:", len(dates)
                )

            for t, i, h, d in zip(title, content, href, dates): 
                
                # Convert epoch in timestamp to datetime
                title = t.text
                content = ''.join(i.text)
                href = h
                timestamp = int(d.get_attribute('data-timestamp'))
                dt_object = datetime.datetime.utcfromtimestamp(timestamp)
                epoch = dt_object.strftime('%Y-%m-%d %H:%M:%S')

            
                result.append(WebPage(
                    website='timesofisrael',
                    url=driver.current_url,
                    title =title,
                    date=epoch,
                    link=href.get_attribute('href'),
                    media_type='liveblog',
                    content=content
                ))
            
            return result
        except Exception as e:
            return f"'Error': {e}, 'title', {scrape_object.title}, 'link', {scrape_object.link} \n"

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



    def run(self):
        homepage = WebPage(link='https://www.timesofisrael.com/', media_type='homepage')
        self.scraper.run(homepage, self.collect_page_titles, 'israeli_times_links')
        with open('output/israeli_times_links.jsonl', 'r') as f:
            for line in f:
                page = json.loads(line)
                page = WebPage(link=page['link'], media_type=page['media_type'])
                if page.media_type == 'article':
                    self.scraper.run(page, self.scrape_article, 'data')
                elif page.media_type == 'liveblog':
                    self.scraper.run(page, self.collect_liveblog, 'data')
                elif page.media_type == 'blog':
                    self.scraper.run(page, self.collect_blogs, 'data')
                
                
                time.sleep(randint(1, 3))

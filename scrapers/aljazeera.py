from core import Database, Logger, WebPage, Scraper
from datetime import datetime, date
import time
from random import randint
from selenium import webdriver
from selenium.webdriver.common.by import By
from core.scraper import Scraper

class AljazeeraScraper():

    def convert_date(self, date_str: str) -> datetime.date:
        for fmt in ("%d %B %Y", "%d %b %Y"):  # Try full and short month names
            try:
                return datetime.strptime(date_str, fmt).date()
            except ValueError:
                continue
        raise ValueError(f"Date format not recognized: {date_str}")

    def collect_page_titles(self, driver, _: WebPage) -> tuple[list[WebPage], bool]:
        try:
            result_date = None

            titles = driver.find_elements(By.XPATH, '//h3[@class="gc__title"]')
            hrefs = driver.find_elements(By.XPATH, '//a[@class="u-clickable-card__link"]')
            dates = driver.find_elements(By.XPATH, '//div[@class="date-simple"]//span[@aria-hidden="true"]')

            result = []
            for title, link, article_date in zip(titles, hrefs, dates):
                href = link.get_attribute('href')
                result_date = self.convert_date(article_date.text)
                            
                result.append(
                    WebPage(
                        website='aljazeera',
                        url=driver.current_url,
                        date=article_date.text,
                        title=title.text,
                        link=href,
                    )
                )


            if result_date < date(2024, 9, 6):
                return result, True

            return result, False
        

        except Exception as e:
           # logger.error(f"Error:", {e})
            return [], False
        


    def collect_newspage(self, driver, _: WebPage) -> tuple[list[WebPage], bool]:
        h = driver.find_elements(By.XPATH, '//main//p')
        title = driver.find_element(By.XPATH, '//header//h1').text
        strings = []
        for i in h:
            strings.append(i.text)
            
        content = ''.join(strings)
        
        y = [WebPage(title=title, content=content)]
        
        print(y)
        
        return y, None

    def run(self):
        homepage = WebPage(link='https://www.aljazeera.com/tag/israel-palestine-conflict/', media_type='homepage')
        Scraper(scrape_object=homepage, scraper_function=self.collect_page_titles, filename='aljazeera_links').run()
        time.sleep(randint(1, 3))



        #news = WebPage(link='https://www.aljazeera.com/news/2025/5/22/lebanese-pm-condemns-wave-of-israeli-attacks-on-southern-lebanon', media_type='homepage')
        #Scraper(scrape_object=news, scraper_function=self.collect_newspage, filename='aljazeera' ).run()


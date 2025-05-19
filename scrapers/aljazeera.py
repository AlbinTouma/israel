from core import Database, Logger, WebPage, Scraper
import datetime
import time
from selenium import webdriver
from selenium.webdriver.common.by import By

class AljazeeraScraper():
    def __init__(self):
        self.scraper = Scraper()

    def convert_date(self, date_str: str) -> datetime.date:
        for fmt in ("%d %B %Y", "%d %b %Y"):  # Try full and short month names
            try:
                return datetime.strptime(date_str, fmt).date()
            except ValueError:
                continue
        raise ValueError(f"Date format not recognized: {date_str}")


    def collect_page_titles(self, driver, _: WebPage, seen_links: set) -> tuple[list[WebPage], bool]:
        try:
            stop_flag = False
            titles = driver.find_elements(By.XPATH, '//h3[@class="gc__title"]')
            hrefs = driver.find_elements(By.XPATH, '//a[@class="u-clickable-card__link"]')
            dates = driver.find_elements(By.XPATH, '//div[@class="date-simple"]//span[@aria-hidden="true"]')

            result = []
            for title, link, article_date in zip(titles, hrefs, dates):
                href = link.get_attribute('href')
                if href not in seen_links:
                    continue

                seen_links.add(href)
            
                
                result.append(
                    WebPage(
                        website='aljazeera',
                        url=driver.current_url,
                        date=article_date.text,
                        title=title.text,
                        link=href,
                    )
                )
                
                result_date = self.convert_date(article_date.text)
                cut_off_date = date(2025, 4, 30) 
                if result_date < cut_off_date:
                    stop_flag = True
                    return result, stop_flag

            return result, stop_flag
        

        except Exception as e:
            logger.error(f"Error:", {e})
            return [], False
        
                        
    def run(self):
        homepage = WebPage(link='https://www.aljazeera.com/tag/israel-palestine-conflict/', media_type='homepage')
        self.scraper.run(homepage, self.collect_page_titles, 'aljazeera_links', incremental=True)
        time.sleep(randint(1, 3))



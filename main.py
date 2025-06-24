#from scrapers.aljazeera import HomePage, LiveBlog, News, ProgramNews
from selenium.webdriver import ChromeOptions
from scrapers.aljazeera.main import AljazeeraScraper
from scrapers.israelitimes import IsraeliTimes, Blog, HomePage, LiveBlog, ScrapeArticle
from core import Logger
import dataclasses as dc
from core import WebPage
import ast
import undetected_chromedriver as uc
from undetected_chromedriver import Chrome, ChromeOptions
from core import DriverClass

driver = DriverClass().get_stealth_driver()

print('\nCollect titles?\n')
user_input = input("Scrape titles: Yes or No \t")
#scraper = IsraeliTimes(user_input, driver)
#scraper.full_run()
AljazeeraScraper = AljazeeraScraper(user_input, driver)
AljazeeraScraper.full_run()

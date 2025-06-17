#from scrapers.aljazeera import HomePage, LiveBlog, News, ProgramNews
from scrapers.aljazeera.main import AljazeeraScraper
from scrapers.israelitimes import IsraeliTimes, Blog, HomePage, LiveBlog, ScrapeArticle
from core import Logger
import dataclasses as dc
from core import WebPage
import ast
import undetected_chromedriver as uc
 


print('\nCollect titles?\n')
user_input = input("Scrape titles: Yes or No \t")

driver  = uc.Chrome(headless=False,use_subprocess=False)
scraper = IsraeliTimes(user_input, driver)
scraper.full_run()

#AljazeeraScraper = AljazeeraScraper()
#AljazeeraScraper.full_run(skip_titles=user_input)

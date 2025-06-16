#from scrapers.aljazeera import HomePage, LiveBlog, News, ProgramNews
from scrapers.aljazeera.main import AljazeeraScraper
from scrapers.israelitimes import IsraeliTimes, Blog, HomePage, LiveBlog, ScrapeArticle
from core import Logger
import dataclasses as dc
from core import WebPage
import ast

#page = WebPage(title='aljazeera',link="https://blogs.timesofisrael.com/an-after-613-enigma/", media_type='blog')



print('\nCollect titles?\n')
user_input = input("Scrape titles: Yes or No")

#scraper = IsraeliTimes()
#scraper.full_run(skip_titles=user_input)

AljazeeraScraper = AljazeeraScraper()
AljazeeraScraper.full_run(skip_titles=user_input)

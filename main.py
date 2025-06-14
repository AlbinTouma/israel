#from scrapers.aljazeera import HomePage, LiveBlog, News, ProgramNews
from scrapers.israelitimes import IsraeliTimes, Blog, HomePage, LiveBlog, ScrapeArticle
from core import Logger
import dataclasses as dc
from core import WebPage
import ner.main


page = WebPage(title='aljazeera',link="https://blogs.timesofisrael.com/an-after-613-enigma/", media_type='blog')

scraper = IsraeliTimes.full_run()


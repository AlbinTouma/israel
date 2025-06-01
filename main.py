#from scrapers.aljazeera import HomePage, LiveBlog, News, ProgramNews
from scrapers.israelitimes import HomePage, LiveBlog, ScrapeArticle
from core import Logger
import dataclasses as dc
from core import WebPage

page = WebPage(title='aljazeera',link="https://www.timesofisrael.com/liveblog-may-12-2025/", media_type='news')

scraper = LiveBlog(scrape_object=page, filename='aljazeera_homepage')

scraper.run()

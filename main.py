#from scrapers.aljazeera import HomePage, LiveBlog, News, ProgramNews
from scrapers.israelitimes import HomePage
from core import Logger
import dataclasses as dc
from core import WebPage

page = WebPage(title='aljazeera',link='https://www.timesofisrael.com/', media_type='news')

scraper = HomePage(scrape_object=page, filename='aljazeera_homepage')

scraper.run()

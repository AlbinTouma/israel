#from scrapers.aljazeera import HomePage, LiveBlog, News, ProgramNews
from scrapers.israelitimes import HomePage, ScrapeArticle
from core import Logger
import dataclasses as dc
from core import WebPage

page = WebPage(title='aljazeera',link='https://www.timesofisrael.com/as-hamas-answers-truce-offer-with-new-demands-witkoff-says-response-totally-unacceptable/', media_type='news')

scraper = ScrapeArticle(scrape_object=page, filename='aljazeera_homepage')

scraper.run()

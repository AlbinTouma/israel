from scrapers.aljazeera import HomePage, LiveBlog, News, ProgramNews
from core import Logger
import dataclasses as dc
from core import WebPage

page = WebPage(title='aljazeera',link="https://www.aljazeera.com/program/newsfeed/2025/5/29/police-clash-with-gaza-war-protesters-at-london-university", media_type='news')

scraper = ProgramNews(scrape_object=page, filename='aljazeera_homepage')
scraper.run()

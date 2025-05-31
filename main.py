from scrapers.aljazeera import HomePage, LiveBlog
from core import Logger
import dataclasses as dc
from core import WebPage

page = WebPage(title='aljazeera',link="https://www.aljazeera.com/tag/israel-palestine-conflict/", media_type='news/liveblog')

scraper = HomePage(scrape_object=page, filename='aljazeera_homepage')
scraper.run()

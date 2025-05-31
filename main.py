from scrapers.aljazeera import HomePage, LiveBlog, News
from core import Logger
import dataclasses as dc
from core import WebPage

page = WebPage(title='aljazeera',link="https://www.aljazeera.com/news/2025/5/30/un-says-famine-stalks-all-in-gaza-israel-shoots-wounds-aid-seekers", media_type='news')

scraper = News(scrape_object=page, filename='aljazeera_homepage')
scraper.run()

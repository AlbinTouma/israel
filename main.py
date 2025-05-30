from scrapers.aljazeera import LiveBlog
from core import Logger
import dataclasses as dc
from core import WebPage

page = WebPage(title='aljazeera', link="https://www.aljazeera.com/news/liveblog/2025/5/24/live-israeli-attacks-kill-76-no-aid-relief-yet-for-besieged-northern-gaza", media_type='news/liveblog')

scraper = LiveBlog(scrape_object=page, filename='aljazeera_liveblog')
scraper.run()

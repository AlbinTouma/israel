from scrapers.aljazeera.main import AljazeeraScraper
from scrapers.israelitimes import Blog, LiveBlog, ScrapeArticle, IsraeliTimes
import scrapers.aljazeera as az
import undetected_chromedriver as uc
from core.models import WebPage 
import pytest

driver  = uc.Chrome(headless=False,use_subprocess=False)

blog = Blog(WebPage(link="https://blogs.timesofisrael.com/oct-7-dawn-french-and-the-dark-arts-of-amnesia-and-illusion/"), 'test', driver)
blog.run()

liveblog = LiveBlog(WebPage(link='https://www.timesofisrael.com/liveblog-june-14-2025/'), 'test', driver)


article = WebPage(link="https://www.timesofisrael.com/three-killed-near-haifa-as-iranian-missile-barrage-targets-northern-israel/")
article = ScrapeArticle(article, 'test', driver)

liveb = WebPage(link='https://www.timesofisrael.com/liveblog-june-14-2025/')
liveblog = LiveBlog(liveb, 'test', driver)

news = WebPage(link='https://www.aljazeera.com/news/2025/6/13/iran-to-double-down-on-nuclear-programme-after-israeli-strikes-analysts')
news_s = az.News(news, 't', driver) 

news_feed = WebPage(link='https://www.aljazeera.com/program/newsfeed/2025/6/13/netanyahu-israel-informed-us-of-iranian-strikes-in-advance')
news_feed_s = az.ProgramNews(news_feed, 't', driver)

liveblog = WebPage(link='https://www.aljazeera.com/news/liveblog/2025/6/12/live-israeli-troops-kill-13-wound-200-in-gaza-in-latest-aid-seeker-attack')
liveblog_s = az.LiveBlog(liveblog, 't', driver)

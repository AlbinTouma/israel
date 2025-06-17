from scrapers.israelitimes import Blog, LiveBlog, ScrapeArticle, IsraeliTimes
import undetected_chromedriver as uc
from core.models import WebPage 
import pytest

driver  = uc.Chrome(headless=False,use_subprocess=False)

blog = Blog(WebPage(link="https://blogs.timesofisrael.com/oct-7-dawn-french-and-the-dark-arts-of-amnesia-and-illusion/"), 'test', driver)
liveblog = LiveBlog(WebPage(link='https://www.timesofisrael.com/liveblog-june-14-2025/'), 'test', driver)
liveblog.run()

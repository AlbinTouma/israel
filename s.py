from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import asyncio
import json
import time


async def scroll_page():
      while True:
        await page.evaluate('window.scrollBy(0, 1000)')
        time.sleep(1)
        current_scroll = await page.evaluate('()=> window.scrollY + window.innerHeight')
        total_height = await page.evaluate('()=> document.body.scrollHeight')
        if current_scroll >= total_height:
            break


async def scrape_page(url:str, locator: str, parsed_entry_function: callable) -> list[dict]:
    data = []
    await page.goto(url)
    await scroll_page()
    blog_div = page.locator(locator)
    count = await blog_div.count()
    for i in range(count):
        item = blog_div.nth(i)
        parsed = await parsed_entry_function(item)
        if parsed:
            data.append(parsed)
    
    return data


async def israel_palestine_conflict_page() -> list[dict]:
    """
    Collects all of the titles, dates, and hrefs from main page and returns them in a list of dicts.
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=50)
        page = browser.new_page()
        page.goto('https://www.aljazeera.com/tag/israel-palestine-conflict/')
        page.is_visible('body')


        try:
            while button := page.locator('button.show-more-button.big-margin'):
                button.scroll_into_view_if_needed()
                html = page.inner_html('body')
                soup = BeautifulSoup(html, 'html.parser')
                contents = soup.find_all('div', {'class': 'gc__content'})
                articles = []
                for content in contents:
                    title = content.find('h3', {'class': 'gc__title'})
                    date = content.find('div', {'class': 'gc__date gc__date--published'})
                    date = date.find('span', attrs={'aria-hidden': 'true'})
                    href = content.find('a', {'class': 'u-clickable-card__link'}, href=True)
        
                    articles.append({
                        'title': title.text,
                        'date': date.text,
                        'href': href['href']
                        })
                    
                

                button.click()
                if len(articles) > 10:
                    return articles
                    break
        except:
            return articles


def scrape_newsfeed(soup):
    # program/newsfeed page. Contains a reels like video and description.
    pass

def scrape_gallery():
    # In pictures is an article
    pass

def scrape_news():
    # News contains longer article
    # news/year/month/day/title
    pass


# I should format time stamp GMT and date


def news_libeblog(page) -> list[dict]:
    """Scrapes the liveblog card feed and collects time, title, text content on cards. Each card is an event. There's also a recap card."""
    while True:
        page.evaluate('window.scrollBy(0, 1000)')
        time.sleep(1)
        current_scroll = page.evaluate('()=> window.scrollY + window.innerHeight')
        total_height = page.evaluate('()=> document.body.scrollHeight')
        if current_scroll >= total_height:
            break
    
    card = page.locator('div.card-live')
    count = card.count()

    result = []
    for i in range(count):
        item = card.nth(i)
        relative_time = item.locator('div.date-relative__time').inner_text()
        title = item.locator('div.card-live__content-area h2').inner_text()
        content = item.locator('div.wysiwyg-content').inner_text()
        
        result.append({
            'time': relative_time,
            'title': title,
            'content': content
            })
    
    del result[-1] # Delete the final item which is always a read our live coverage card
    return result
 



with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=50)
    page = browser.new_page()
    page.goto('https://www.aljazeera.com')
    
    pages: list[dict] = scrape_page(
        url='https://www.aljazeera.com',
        locator='body',
        parsed_entry_function=scrape_article_urls,
    )

        




    


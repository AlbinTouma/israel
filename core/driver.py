from selenium.webdriver import ChromeOptions
#from core import Logger
import dataclasses as dc
from core import WebPage
import ast
import undetected_chromedriver as uc
from undetected_chromedriver import Chrome, ChromeOptions

class DriverClass:

    @staticmethod
    def get_stealth_driver(headless=False):
        options = ChromeOptions()
        options.page_load_strategy = 'eager'
        #options.add_argument("--disable-blink-features=AutomationControlled")
        #options.add_argument("--no-sandbox")
       # options.add_argument("--disable-dev-shm-usage")
       # options.add_argument("--disable-notifications")
       # prefs = {
       #     "profile.managed_default_content_settings.images": 2,
       #     "profile.managed_default_content_settings.fonts": 2,
       #     "profile.managed_default_content_settings.stylesheets": 2,
        #    "profile.managed_default_content_settings.plugins": 2,
     #   }
     #   options.add_experimental_option("prefs", prefs)
        if headless:
            options.add_argument("--headless=new")

        driver  = Chrome(options=options, use_subprocess=False)
        driver.set_page_load_timeout(30)
        return driver

    @staticmethod
    def is_driver_alive(driver):
        try:
            _ = driver.title
            return True

        except Exception as e:
            print("DATACLASS ERR", e)
            return False


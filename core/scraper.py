from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import json
import undetected_chromedriver as uc
import time
from random import randint
import dataclasses as dc
from datetime import datetime, date
from pathlib import Path
from .models import WebPage


class Scraper:
    def click_show_more_button(self, driver) -> bool:
        try:
            button = driver.find_element(By.XPATH, '//button[@class="show-more-button big-margin"]')
            if button.is_displayed():
                button.click()
                time.sleep(1)
                return True
        
        except Exception as e:
            pass
        return False
            
    def scroll_method(self, driver, scraper_function=None, scrape_object=None, filename=None):
        try:
            last_height = driver.execute_script("return document.body.scrollHeight")
            same_height_count = 0
            button_pressed_count = 0
            seen_links = set()

            while True:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(1)

                button_clicked = self.click_show_more_button(driver)
                if button_clicked:
                    button_pressed_count += 1

                if scraper_function and scrape_object:
                    result, stop_flag = scraper_function(driver, scrape_object, seen_links)
                    self.write_to_jsonl(result, filename)
                    if stop_flag:
                      #  logger.info("Criteria met, terminating infinity scroll.")
                        break

    
                new_height = driver.execute_script("return document.body.scrollHeight")
            
                if new_height == last_height:
                    same_height_count += 1
                    if same_height_count >= 3:
                       # logger.info("Reached the end of the page.")
                        break
                else:
                    same_height_count = 0
                    last_height = new_height
                    

        except Exception as e:
            print("Error:", e)

        
    def write_to_jsonl(self, result: list[WebPage] | WebPage | Exception, filename: str):
        """Writes the result of the scraper function to a jsonl file. 
        If result is a list, each element is written to the file. 
        If result is a dict, it is written as a single line.
        """
        CURRENT_DIR = Path().resolve()
        PROJECT_ROOT = CURRENT_DIR.parent
        #PROJECT_ROOT = Path(__file__).resolve().parent.parent  # Adjust as needed

        output_dir = PROJECT_ROOT / 'output'
        output_dir.mkdir(exist_ok=True)  # Create it if it doesn't exist
        logs_dir = PROJECT_ROOT / 'logs'
        logs_dir.mkdir(exist_ok=True)  # Create it if it doesn't exist

        # Check if the file already exists
        if not (output_dir / f'{filename}.jsonl').exists():
            with open(f'{output_dir}/{filename}.jsonl', 'w') as f:
                f.write('')
                f.close()
        if not (logs_dir / f'{filename}_error.jsonl').exists():
            with open(f'{logs_dir}/{filename}_error.jsonl', 'w') as f:
                f.write('')
                f.close()
        if not (logs_dir / f'{filename}_captcha.jsonl').exists():
            with open(f'{logs_dir}/{filename}_captcha.jsonl', 'w') as f:
                f.write('')
                f.close()
        


        if result:
            with open(f'{output_dir}/{filename}.jsonl', 'a') as f:        
                if isinstance(result, list):
                    result = [dc.asdict(r) for r in result]
                    [f.write(json.dumps(r, ensure_ascii=False) + '\n') for r in result]

                elif isinstance(result, WebPage):
                    f.write(json.dumps(dc.asdict(result), ensure_ascii=False) + '\n')
                    f.close()
        
                elif isinstance(result, Exception):
                    with open(f'{logs_dir}/{filename}_error.jsonl', 'a') as f:
                        f.write(json.dumps({'error': str(result)}, ensure_ascii=False) + '\n')
                        f.close()

        else:
            with open(f'{logs_dir}/{filename}_captcha.jsonl', 'a') as f:
                if isinstance(result, list):
                    for r in result:
                        f.write(r + '\n')
                    f.close()
                else:    
                    f.write(result + '\n')
                    f.close()

    def run(self, scrape_object: WebPage, scraper_function, filename: str, incremental: bool):
        # This function is used to run the scraper
        self.driver  = uc.Chrome(headless=False,use_subprocess=False)
        self.driver.get(scrape_object.link)

        ## If page is infinite scroll, we scroll down to the page, write results, press button, and repeat until stop condition is met.
        if incremental:
            self.scroll_method(
                driver=self.driver,
                scraper_function=scraper_function,
                scrape_object=scrape_object,
                filename=filename
            )

        else:
            self.scroll_method(driver=self.driver)
            result =  scraper_function(self.driver, scrape_object)
            self.write_to_jsonl(result, filename)
        
        self.driver.quit()

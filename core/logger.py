import dataclasses
import logging

class Logger:
    def run():
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        file_handler = logging.FileHandler('scraper.log')
        file_handler.setLevel(logging.INFO)
        # Create a formatter and set it for the handler
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        # Add the handler to the logger
        logger.addHandler(file_handler)


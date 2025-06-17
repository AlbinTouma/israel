import dataclasses
import logging

class Logger:
    def __init__(self):
        self.errlog = self.setup_logger(name='errlog', filename='logs/errlog.log')
        self.log = self.setup_logger(name='log', filename='logs/ouput.log')
    
    def setup_logger(self, name, filename):
            logger = logging.getLogger(name)
            if not logger.handlers:
                logger.setLevel(logging.DEBUG)
                Format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
                fh = logging.FileHandler(filename)
                fh.setFormatter(Format)
                logger.addHandler(fh)
            return logger

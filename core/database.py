import json
from .models import WebPage
from pathlib import Path
import dataclasses as dc
import hashlib

class Database:

    @staticmethod
    def generate_unique_id(title: str, url: str) -> str:
        combined = (title + url).encode('utf-8')
        unique_id = hashlib.md5(combined).hexdigest()  # or use sha256
        return unique_id

    @staticmethod
    def check_if_exists(link: str, filename) -> bool:
        # This function is used to check if the link already exists in the database
        with open(f'../output/{filename}.jsonl', 'r') as f:
            for line in f:
                if json.loads(line)['link'] == link:
                    return True
        return False
    
    @staticmethod
    def read_jsonl(filename: str) -> list[dict]:
        r = []

        with open(f"output/{filename}.jsonl", 'r') as reader:
            for index, row in enumerate(reader):       
                try:
                            json_row = json.loads(row)
                            r.append(json_row)
                except json.decoder.JSONDecodeError as e:
                    continue
                        
        return r
    
    @staticmethod
    def to_dict(obj: WebPage):
        return {
            "website": obj.website, 
            "url": obj.url,
            "title": obj.title,
            "date": obj.date,
            "media_type": obj.media_type,
            "link": obj.link,
            "content": obj.content,
       }

    @staticmethod
    def write_to_jsonl(result: list[WebPage] | WebPage | Exception, filename: str):
        """Writes the result of the scraper function to a jsonl file. 
        If result is a list, each element is written to the file. 
        If result is a dict, it is written as a single line.
        """
        PROJECT_ROOT = Path(__file__).resolve().parent.parent 
        output_dir = PROJECT_ROOT / 'output'
        output_dir.mkdir(exist_ok=True)  # Create it if it doesn't exist
        logs_dir = PROJECT_ROOT / 'logs'
        logs_dir.mkdir(exist_ok=True)  # Create it if it doesn't exist


        if result:
            with open(f'{output_dir}/{filename}.jsonl', 'a') as f:        
                if isinstance(result, list):
                    result = [Database.to_dict(r) for r in result]
                    for ddict in result:
                        jout = json.dumps(ddict) + '\n'
                        f.write(jout)
                    f.close()

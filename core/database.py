import json
from .models import WebPage
from pathlib import Path
import dataclasses as dc


class Database:
    def check_if_exists(link: str, filename) -> bool:
        # This function is used to check if the link already exists in the database
        with open(f'../output/{filename}.jsonl', 'r') as f:
            for line in f:
                if json.loads(line)['link'] == link:
                    return True
        return False
    
    def write_to_jsonl(result: list[WebPage] | WebPage | Exception, filename: str):
        """Writes the result of the scraper function to a jsonl file. 
        If result is a list, each element is written to the file. 
        If result is a dict, it is written as a single line.
        """
        #CURRENT_DIR = Path().resolve()
        #PROJECT_ROOT = CURRENT_DIR.parent
        PROJECT_ROOT = Path(__file__).resolve().parent.parent 
        print(PROJECT_ROOT) # Adjust as needed

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

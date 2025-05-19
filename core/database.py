import json


class Database:
    def check_if_exists(link: str, filename) -> bool:
        # This function is used to check if the link already exists in the database
        with open(f'../output/{filename}.jsonl', 'r') as f:
            for line in f:
                if json.loads(line)['link'] == link:
                    return True
        return False    

# This script formats the scraped articles in a csv that label-studio can accept.

from core.database import Database
import json

df = Database.read_jsonl('aljazeera_data')

d = []
for i in df:
    d.append({"data": {"title": i.get('title'), "textlabel": i.get('content')}})

with open('annotations/o.json', 'w') as fp:
    r = json.dump(d, fp)


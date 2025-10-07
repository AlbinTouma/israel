# Label-Studio requires a certain format when uploading json or csv for annotation.
# This script formats the scraped articles as either a csv or json that label-studio accepts.
# Output is saved to annotations folder as: {project name}_annotation_tasks

from core.database import Database
import json
import pandas as pd


class ConvertLabels():

    @staticmethod
    def ConvertJSONL(file):
        df = Database.read_jsonl(file)
        d = []
        for i in df:
            d.append({"data": {"title": i.get('title'), "textlabel": i.get('content')}})

        with open(f'labelling/tasks/{file}_annotation_tasks.json', 'w') as fp:
            r = json.dump(d, fp)

    @staticmethod    
    def ConvertCSV(file):
        df = pd.read_csv(file)
        print(df.columns)
        d = []
        for i, row in df.iterrows():
            print(i)
            d.append({'data': {'title': row['title'], 'textlabel': row['content']}})


        with open(f'labelling/tasks/{file}_annotation_tasks.json', 'w') as fp:
            r = json.dump(d, fp)



ConverterClass = ConvertLabels()

type_file = input('Decide on format you want output to be in and type JSON or CSV \n')
fileName = input('What is your file called?')

match type_file:
    case 'JSON':
        ConverterClass.ConvertJSONL(fileName)
    case 'CSV':
        ConverterClass.ConvertCSV(fileName)
    
    case _:
        print("That's not a valid input")

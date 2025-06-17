import json
import pandas as pd
import nltk
import re
nltk.data.path = ['/home/albin/nltk_data']
nltk.download('punkt_tab')
nltk.download('averaged_perceptron_tagger_eng')
from pathlib import Path
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.data import find
find("tokenizers/punkt")






class Debug:
    def read_jsonl_to_df(filename: str) -> pd.DataFrame:
        r = []
        with open(f"../output/{filename}.jsonl", 'r') as reader:
            for row in reader:
                json_row = json.loads(row)
                r.append(pd.DataFrame(json_row, index=[0]))
            
        df = pd.concat(r, ignore_index=True)
        duplicates = df[df.duplicated() == True]
        data   = df.drop_duplicates()
        return data


class Statistics:
    def __init__(self, filename: str):
        self.filename = filename
     
    def average_stats(self, data: pd.DataFrame) -> None:
        data['words'] = data['content'].apply(lambda x: len(x.split()))
        data['chars'] = data['content'].apply(lambda x: len(x))
        data['sentences'] = data['content'].apply(lambda x: len(x.split('.')))
        data['paragraphs'] = data['content'].apply(lambda x: len(x.split('\n')))
        data['avg_word_length'] = data['chars'] / data['words']
        result = data.groupby('media_type').agg({'sentences': 'mean', 'words': 'mean', 'chars': 'mean', 'paragraphs': 'mean', 'avg_word_length': 'mean'}).reset_index().round(0)
        
        print(
        "N sample: %s \n\n"
        "Average lenght of words, sentences, paragraphs:" \
        "\n\n %s" %(len(data), result), end="\n\n"
        )

    def nltk_stats(self, title, sentence) -> None:
        print("nltk.data.paths: ", nltk.data.path)

        stop_words = nltk.corpus.stopwords.words('english')
        tokens: list = nltk.word_tokenize(sentence)
        filtered_sentence = [w for w in tokens if not w.lower() in stop_words]
        tagged: list[tuple] = nltk.pos_tag(filtered_sentence)
        nouns = [word for word, pos in tagged if pos in ['NNP']]
        for noun in nouns:
            print(
            "Title: %s \n",
            {"Entity": noun,
            "Sentence": sentence,
            }
            )
    
    def run(self):
        data: pd.DataFrame = Debug.read_jsonl_to_df(self.filename)
        self.average_stats(data)
        for i in data.iterrows():
            self.nltk_stats(i[1]['title'], i[1]['content'])
        

Statistics('aljazeera').run()
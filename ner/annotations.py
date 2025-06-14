
def create_annotation(df):

    df = Database.read_jsonl('israelitimes_data')
    for i in df:
       with open('annotations/text_class.text', 'a') as fp:
            title = i.get('title')
            if title:
                fp.write(f'{title},\n')



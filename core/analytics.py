import pandas as pd

links = pd.read_json('output/israelitimes_links.jsonl', lines=True)
data = pd.read_json('output/israelitimes_data.jsonl', lines=True)

df = pd.merge(links, data, on='link', how='outer')

success_count = df['link'].isna().value_counts().reset_index()
success_rate = df['link'].isna().value_counts(normalize=True).reset_index()
success = pd.merge(success_count, success_rate)

print(f'\nHow many failed? (True = Failed) \n {success}\n')

print(df[df['link'].isna() == True][['link', 'content_y']])
y = df[df['link'].isna() == True].reset_index()
print(y['media_type_x'].value_counts())

x = pd.DataFrame({'Links': df['media_type_x'].value_counts(), 'Data': df['media_type_y'].value_counts()})
x['To scrape'] = x['Links'] - x['Data']
print(x)




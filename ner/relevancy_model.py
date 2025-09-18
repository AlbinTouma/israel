# Relevancy model predicts if an article is relevant using binary classification models

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
import pandas as pd
import numpy as np
import numpy as np
from nltk.corpus import stopwords

df = pd.DataFrame.dropna(pd.read_csv('annotations/annotated_.csv'))
text = df['textlabel']
labels = df['sentiment']

# Encode the labels
label_encoder = LabelEncoder()
labels_enc = label_encoder.fit_transform(labels)

# Split into test and training data
X_train, X_test, y_train, y_test = train_test_split(text, labels_enc, test_size=0.20)


# Init pipeline
stopwords = stopwords.words('english')
pipeline = Pipeline([
    ("vectorizer", TfidfVectorizer(lowercase=True, stop_words=stopwords, ngram_range=(1,2))),
    ("classifier", LinearSVC())
])


pipeline.fit(X_train, y_train)

# Train pipeline
y_pred = pipeline.predict(X_test)


# Load articles
df_all = pd.read_json('output/aljazeera_data.jsonl', lines=True)

# Create predictions
df_all['prediction'] = pipeline.predict(df_all['content'])

df_relevant = df_all.query('prediction > 0')

df_relevant.to_csv('output/relevant_articles.csv')

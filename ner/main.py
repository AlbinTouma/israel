import numpy as np
from pandas.core.common import random_state
from collections import Counter
import json
import tensorflow as tf
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
import pandas as pd
import matplotlib.pyplot as plt
import tensorflow as tf
from core import Database
from .ml_models import MLModelling
from .vectorize import VectorizeText

def read_annotated_data():
    return pd.DataFrame.dropna(pd.read_csv('annotations/annotated.csv'))

def split_data(data, labels):
    return train_test_split(data, labels, test_size=0.25, stratify=labels)


df = read_annotated_data()
vec_cls = VectorizeText(df['textlabel'], df['sentiment'])
vec_cls.encode_label()
training_data, testing_data, training_labels, testing_labels = split_data(vec_cls.data, vec_cls.labels) 
training_data, testing_data = vec_cls.create_bag_of_words(training_data, testing_data)

ML_cls = MLModelling(training_data, training_labels, testing_data, testing_labels)
ML_cls.compare_models()
ML_cls.classification_report(vec_cls)


quit()

# Cross validation scores
scores = cross_val_score(classifier, titles_train_vec, labels_encoded_train, cv=5, scoring='f1') 
plt.bar([0,1,2,3,4], height=scores)
plt.title("Cross Validation", loc='left')
plt.xlabel('Iteration')
plt.ylabel('Scores of estimator')
plt.show()

f = open('annotations/o.json')
f = json.load(f)


data = pd.json_normalize(f)
v = data['data.textlabel']

for title in v:
    title_v = vectorizer.transform([title])
    y_pred = classifier.predict(title_v)
    y_prob = classifier.predict_proba(title_v)
    with open('annotations/results_content.csv', 'a') as f:
        f.write(f'{title}\t{le.inverse_transform(y_pred)}\t{y_prob} \n')

   # print(title, 'Predicted label', le.inverse_transform(y_pred), y_prob)



quit()
with open('output/o.jsonl', 'r') as f:
    lines = f.readlines() 

v = [json.loads(l) for l in lines]
v = [l.get('title') for l in v]

for title in v:
    title_v = vectorizer.transform([title])
    y_pred = classifier.predict(title_v)
    y_prob = classifier.predict_proba(title_v)
    with open('annotations/results.csv', 'a') as f:
        f.write(f'{title}\t{le.inverse_transform(y_pred)}\t{y_prob} \n')




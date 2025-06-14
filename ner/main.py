import numpy as np
from pandas.core.common import random_state
from sklearn.metrics import classification_report
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
from sklearn.metrics import ConfusionMatrixDisplay, confusion_matrix
from sklearn.model_selection import cross_val_score
import eli5

df = pd.read_csv('annotations/annotated.csv')

df['sentiment'].value_counts()

# Encode our labels
le = LabelEncoder()
le.fit(df['sentiment'])
labels_encoded = le.transform(df['sentiment'])

# Create training,  testing
titles_train, titles_test, labels_encoded_train, labels_encoded_test = train_test_split(df['text'], labels_encoded, test_size=0.25, stratify=labels_encoded)

# Bag of Words
vectorizer = CountVectorizer(lowercase=False)
titles_train_vec = vectorizer.fit_transform(titles_train)
titles_test_vec = vectorizer.transform(titles_test)


# Logistic Regression Model
classifier = LogisticRegression(class_weight='balanced')
classifier.fit(titles_train_vec, labels_encoded_train)
predictions = classifier.predict(titles_test_vec)
print(classification_report(labels_encoded_test, predictions, target_names=le.classes_))


# Docs for confusion matrix: https://scikit-learn.org/stable/modules/generated/sklearn.metrics.ConfusionMatrixDisplay.html#sklearn.metrics.ConfusionMatrixDisplay
cm = confusion_matrix(labels_encoded_test, predictions, labels=classifier.classes_)
cm_display = ConfusionMatrixDisplay(cm).plot()

# Explain weights tells me what words push towards relevant/irrelevant
eli5.explain_weights(classifier, vec=vectorizer) #show=['targets', 'description', 'feature_importances'])classifier.coef_	


# Cross validation scores
scores = cross_val_score(classifier, titles_train_vec, labels_encoded_train, cv=5, scoring='f1') 
plt.bar([0,1,2,3,4], height=scores)
plt.title("Cross Validation", loc='left')
plt.xlabel('Iteration')
plt.ylabel('Scores of estimator')






with open('output/israelitimes_data.jsonl', 'r') as f:
    lines = f.readlines() 

v = [json.loads(l) for l in lines]
v = [l.get('title') for l in v]

for title in v:
    title_v = vectorizer.transform([title])
    y_pred = classifier.predict(title_v)
    y_prob = classifier.predict_proba(title_v)
    with open('results.csv', 'a') as f:
        f.write(f'{title}\t{le.inverse_transform(y_pred)}\t{y_prob} \n')

    print(title, 'Predicted label', le.inverse_transform(y_pred), y_prob)



import json
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
import pandas as pd
from .ml_models import MLModelling
from .vectorize import VectorizeText
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from nltk.corpus import stopwords

stopwords = stopwords.words('english')
models = {
        "Logistic Regression": LogisticRegression(), 
        "Support Vector Machines": LinearSVC(), 
        "Decision Trees": DecisionTreeClassifier(), 
        "Random Forest Classifier": RandomForestClassifier(), 
        "Naive Bayes": GaussianNB(), 
        "K-Nearest Neighbor": KNeighborsClassifier()
}

vectorizers = {
    "BagOfWords": CountVectorizer(lowercase=True,stop_words=stopwords, ngram_range=(1,2)),
    "TFIDF": TfidfVectorizer(lowercase=True, stop_words=stopwords, ngram_range=(1,2))
}

df = pd.DataFrame.dropna(pd.read_csv('annotations/annotated.csv'))
text = df['textlabel']
labels = df['sentiment']

all_results = []
for vec_name, vec_instance in vectorizers.items():

    vec = VectorizeText(vec_instance)
    encoded_labels =vec.encode_label(labels)

    X_train, X_test, y_train, y_test = vec.split_and_vectorize(text, encoded_labels)
    #Train models
    ml = MLModelling(models)
    results_df = ml.train_and_evaluate(X_train, y_train, X_test, y_test)

    for _, row in results_df.iterrows():
        all_results.append({
            "Vectorizer": vec_name,
            "Classifier": row['Model'],
            "Accuracy": row['Accuracy'],
            "F1": row['F1'],
            "Recall": row['Recall']
        })

x = vec.vectorizer.get_feature_names_out()
coef = ml.trained_models['Logistic Regression'].coef_[0]
w = pd.DataFrame({"Model": "Logsitic Regression", "Word": x, "Weight": coef}).sort_values(by='Weight', ascending=False)
print(f'{w.head(10)} \n {w.tail(10)}')

final_df = pd.DataFrame(all_results)
print(final_df)

data = pd.read_json('output/aljazeera_data.jsonl', lines=True)
text = data['content']
X_new = vec.vectorizer.transform(text)
trained_classifier = ml.trained_models['Decision Trees']
pred = trained_classifier.predict(X_new)

r = pd.DataFrame({'title': data['title'], 'content': text, "pred": pred, "link": data['link'], "media_type": data['media_type']})
r = r[r['pred'] == 1]
r.to_json('result.json', orient='records')
print(r)


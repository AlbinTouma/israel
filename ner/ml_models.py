from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score
from sklearn.metrics import ConfusionMatrixDisplay, confusion_matrix
import pandas as pd
# https://www.learndatasci.com/glossary/binary-classification/ provides useful guide to evaluating performance of model.
from dataclasses import dataclass
from sklearn.metrics import classification_report
from sklearn.metrics import ConfusionMatrixDisplay, confusion_matrix
from sklearn.model_selection import cross_val_score
import eli5

models = {
    "classification_models":{
        "Logistic Regression": LogisticRegression(), 
        "Support Vector Machines": LinearSVC(), 
        "Decision Trees": DecisionTreeClassifier(), 
        "Random Forest Classifier": RandomForestClassifier(), 
        "Naive Bayes": GaussianNB(), 
        "K-Nearest Neighbor": KNeighborsClassifier()
    }
}

class MLModelling:
    models = models

    def __init__(self, training_data, training_labels, test_data, test_labels):
        self.training_data = training_data
        self.training_labels = training_labels
        self.test_data = test_data
        self.test_labels = test_labels

    def compare_models(self):
        accuracy, precision, recall = {}, {}, {}
        models = MLModelling.models['classification_models']

        for key in models.keys():
            models[key].fit(self.training_data.toarray(), self.training_labels)
            predictions = models[key].predict(self.test_data.toarray())
            accuracy[key] = accuracy_score(predictions, self.test_labels)
            precision[key] = precision_score(predictions, self.test_labels)
            recall[key] = recall_score(predictions, self.test_labels)

        df_model = pd.DataFrame({"Accuracy": accuracy.values(), "Precision": precision.values(), "Recall": recall.values()}, index=models.keys())
        print(df_model)

    def classification_report(self, vec_cls):
        classifier = LogisticRegression(class_weight='balanced')
        classifier.fit(self.training_data, self.training_labels)
        predictions = classifier.predict(self.test_data)
        report = classification_report(self.test_labels, predictions, target_names=vec_cls.encoder.classes_)

        cm = confusion_matrix(self.test_labels, predictions, labels=classifier.classes_)
        ConfusionMatrixDisplay(cm, display_labels=['irrelevant', 'relevant']).plot()

        eli5.explain_weights(classifier, vec=vec_cls.encoder) #show=['targets', 'description', 'feature_importances'])classifier.coef_	






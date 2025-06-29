from sklearn.metrics import accuracy_score, precision_score, recall_score
from sklearn.metrics import ConfusionMatrixDisplay, confusion_matrix
import pandas as pd
from dataclasses import dataclass
from sklearn.metrics import classification_report
from sklearn.metrics import ConfusionMatrixDisplay, confusion_matrix
from sklearn.model_selection import cross_val_score
import eli5
import matplotlib.pyplot as plt
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report,
)

class MLModelling:
    def __init__(self, models: dict):
        self.models = models
        self.trained_models = {}

    def train_and_evaluate(self, X_train, y_train, X_test, y_test):
        results = []
        for name, model in self.models.items():
            model.fit(X_train.toarray(), y_train)
            preds = model.predict(X_test.toarray())
            self.trained_models[name] = model
            results.append({
                "Model": name, 
                "Accuracy": accuracy_score(y_test, preds),
                "Precision": precision_score(y_test, preds),
                "Recall": recall_score(y_test, preds),
                "F1": f1_score(y_test, preds)
            })
        return pd.DataFrame(results)
    
    def confusion_matrix(self, model_name, X_test, y_test, label_encoder) -> dict:
        print("Confusion Matrix")
        model = self.trained_models.get(model_name)
        if model is None: 
            print("Model not trained", model_name)

        predictions = model.predict(X_test)
        return classification_report(y_test, predictions, target_names=label_encoder, output_dict=True)

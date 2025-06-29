from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

class VectorizeText():
    def __init__(self, vectorizer):
        self.vectorizer = vectorizer
        self.label_encoder = LabelEncoder()

    def encode_label(self, labels):
        """Encode labels from categorical to int"""
        return self.label_encoder.fit_transform(labels)

    def split_and_vectorize(self,texts,labels,test_size=0.25, stratify=True):
        stratify_labels = labels if stratify else None

        X_train, X_test, y_train, y_test = train_test_split(
        texts,
        labels,
        test_size=test_size,
        stratify=stratify_labels
        )
        X_train_vect = self.vectorizer.fit_transform(X_train)
        X_test_vect = self.vectorizer.transform(X_test)
        return X_train_vect, X_test_vect, y_train, y_test

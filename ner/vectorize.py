from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import CountVectorizer

class VectorizeText():

    BagOfWords = CountVectorizer(lowercase=False)

    def __init__(self, data, labels):
        self.labels = labels
        self.data = data
        self.encoder = LabelEncoder()

    def encode_label(self):
        """Encode labels from categorical to int"""

        self.encoder.fit(self.labels)
        encoded = self.encoder.transform(self.labels)
        self.labels = encoded

    def create_bag_of_words(self,train, test):
        return(VectorizeText.BagOfWords.fit_transform(train), VectorizeText.BagOfWords.transform(test))


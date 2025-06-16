from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier

# https://www.learndatasci.com/glossary/binary-classification/ provides useful guide to evaluating performance of model.

classification_models = {
    "Logistic Regression": LogisticRegression(), 
    "Support Vector Machines": LinearSVC(), 
    "Decision Trees": DecisionTreeClassifier(), 
    "Random Forest Classifier": RandomForestClassifier(), 
    "Naive Bayes": GaussianNB(), 
    "K-Nearest Neighbor": KNeighborsClassifier()
}



from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.externals import joblib
import pandas as pd

#loading the dataset 
data = pd.read_csv("data.csv")

#splitting the dataset into X, y
X = data['message']
y = data['interest']

# Initialize the vectorizer
vectorizer = CountVectorizer()

# Vectorize the messages
X = vectorizer.fit_transform(X)

# Initialize the classifier
clf = MultinomialNB()

# Train the classifier
clf.fit(X, y)

#save the model and the vectorizer
joblib.dump(clf, 'model.pkl')
joblib.dump(vectorizer, 'vectorizer.pkl')


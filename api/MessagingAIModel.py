from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.externals import joblib
import numpy as np

class InterestPredictor:
    def __init__(self):
        self.model = None
        self.vectorizer = None
        self.user_interests = {}
        self.load_model()

    def load_model(self):
        self.model = joblib.load('model.pkl')
        self.vectorizer = joblib.load('vectorizer.pkl')

    def predict_interests(self, message, user_id):
        #Vectorize the message
        message = self.vectorizer.transform([message])
        #predict the interest
        interest = self.model.predict(message)
        if user_id in self.user_interests:
            self.user_interests[user_id].append(interest)
        else:
            self.user_interests[user_id] = [interest]

    def get_user_interests(self, user_id):
        if user_id in self.user_interests:
            return self.user_interests[user_id]
        else:
            return None

    def get_interesting_stories(self, user_id):
        user_interests = self.get_user_interests(user_id)
        if user_interests:
            stories = []
            for interest in user_interests:
                # Use the user's interests to fetch personalized stories
                # e.g. stories = StoryFetcher.fetch_stories(interest)
                stories.extend(StoryFetcher.fetch_stories(interest))
            return stories
        else:
            return None

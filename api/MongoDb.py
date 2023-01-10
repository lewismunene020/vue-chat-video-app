from pymongo import MongoClient

class Database:
    def __init__(self):
        self.client = MongoClient()
        self.db = self.client.chat_app_db
        self.messages = self.db.messages

    def store_message(self, message, user_id):
        self.messages.insert_one({"message": message, "user_id": user_id})

    def fetch_messages(self, user_id):
        return self.messages.find({"user_id": user_id})

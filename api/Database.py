import mysql.connector

class Database:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None

    def connect(self):
        self.connection = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )
        print("Connection established.")

    def close(self):
        if self.connection:
            self.connection.close()
            print("Connection closed.")

    def insert_message(self, text, sender, timestamp, chat_id):
        cursor = self.connection.cursor()
        query = "INSERT INTO messages (text, sender, timestamp, chat_id) VALUES (%s, %s, %s, %s)"
        values = (text, sender, timestamp, chat_id)
        cursor.execute(query, values)
        self.connection.commit()
        print("Message inserted.")

    def fetch_messages(self, chat_id):
        cursor = self.connection.cursor()
        query = "SELECT * FROM messages WHERE chat_id=%s"
        cursor.execute(query, (chat_id,))
        messages = cursor.fetchall()
        print("Messages fetched.")
        return messages

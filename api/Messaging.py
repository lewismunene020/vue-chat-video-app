from flask import Flask, jsonify, request
from flask_socketio import SocketIO
from Database import Database

app = Flask(__name__)
socketio = SocketIO(app)

db = Database("host", "user", "password", "database")
db.connect()

@socketio.on('connect')
def connect():
    print('Client connected')

@socketio.on('disconnect')
def disconnect():
    print('Client disconnected')

@socketio.on('sendMessage')
def handle_send_message(json):
    message = json['message']
    db.insert_message(message['text'], message['sender'], message['timestamp'], message['chatId'])
    messages = db.fetch_messages(message['chatId'])
    emit('receiveMessage', { 'messages': messages }, broadcast=True)
    
if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=3000)

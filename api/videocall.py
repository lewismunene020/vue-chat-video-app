from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

users = []

@socketio.on('connect')
def connect():
    print('Client connected')

@socketio.on('startCall')
def start_call(data):
    print('Call started')
    room = json.loads(data)
    join_room(room['id'])
    emit('callStarted', room=room['id'])

@socketio.on('callAccepted')
def call_accepted(data):
    print('Call Accepted')
    emit('callAccepted', room=data['room'])

@socketio.on('sendStream')
def send_stream(data):
    print('Stream received')
    stream_data = json.loads(data)
    emit('incomingStream', {'stream': stream_data['stream'], 'room': stream_data['room']}, room=stream_data['room'])

@socketio.on('endCall')
def end_call(data):
    print('Call ended')
    emit('callEnd', room=data['room'])

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=3000)

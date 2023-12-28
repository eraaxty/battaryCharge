# app/socketio_events.py
from flask_socketio import emit
from app import socketio
from app.mqtt import messages

@socketio.on('connect')
def handle_connect():
    if messages:
        brocker_message = messages[-1]
        emit('sse_message', {'message': brocker_message})
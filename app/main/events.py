from flask import session
from flask.ext.socketio import emit, join_room, leave_room
from .. import socketio
from ..models import Message
from datetime import datetime
from app import db

@socketio.on('joined')
def joined(message):
    """Sent by clients when they enter a room.
    A status message is broadcast to all people in the room."""
    room = session.get('room')
    join_room(room)
    user_name = session.get('name')
    msg = CreateAddMessage(' has entered the room.', room, user_name, True)
    emit('status', {'msg': msg }, room=room)

@socketio.on('text')
def send(message):
    """Sent by a client when the user entered a new message.
    The message is sent to all people in the room."""
    room = session.get('room')
    user_name = session.get('name')
    if len(message['msg']) > 0:
        msg = CreateAddMessage(message['msg'], room, user_name)
        emit('message', {'msg': msg}, room=room)

@socketio.on('news')
def send_news(message):
    """Sent by a client when the user entered a new message.
    The message is sent to all people in the room."""
    room = session.get('room')
    user_name = 'News'
    msg = message['msg']
    emit('message', {'msg': msg, 'name': user_name}, room=room)

@socketio.on('left')
def left(message):
    """Sent by clients when they leave a room.
    A status message is broadcast to all people in the room."""
    room = session.get('room')
    user_name = session.get('name')
    leave_room(room)
    msg = CreateAddMessage(' has left the room.', room, user_name, True)
    emit('status', {'msg': msg }, room=room)


def CreateAddMessage(text, room, user, is_status=False):
    if (is_status):
        text = user + text
    else:
        text = user + ": " + text
    msg = Message(text, room, user, datetime.utcnow())
    db.session.add(msg)
    db.session.commit()
    return text
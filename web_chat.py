from flask import Flask
from app import create_app, socketio
from app.models import Room, Message
from flask.ext.whooshalchemy import whoosh_index
# create app instance with the selected configuration
app = create_app('default')
whoosh_index(app, Room)
whoosh_index(app, Message)

if __name__ == '__main__':
    socketio.run(app) #host='192.168.1.3'
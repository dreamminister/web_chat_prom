from flask import Flask
from app import create_app, socketio
# create app instance with the selected configuration
app = create_app('default')

if __name__ == '__main__':
    socketio.run(app, host='192.168.1.3')

from flask import Flask
from app import create_app
# create app instance with the selected configuration
app = create_app('default')

if __name__ == '__main__':
    app.run()

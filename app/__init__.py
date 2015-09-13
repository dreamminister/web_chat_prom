from flask import Flask
from flask.ext.bootstrap import Bootstrap
from flask.ext.sqlalchemy import SQLAlchemy
from config import config, basedir
from flask.ext.login import LoginManager
import os

bootstrap = Bootstrap()
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    bootstrap.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)

    from main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    # Checking if our db exists, creating and supplying initial data if it doesn't.
    # NOTE: this will work fine only for SQLite engine (the db file is saved on disk).
    if not os.path.exists(os.path.join(basedir, config[config_name].DATABASE_NAME)):
        with app.app_context():
            db.create_all()
            db.session.commit()

    return app
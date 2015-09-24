import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dreamminister'
    DATABASE_NAME = 'data-dev.sqlite'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
    'sqlite:///' + os.path.join(basedir, DATABASE_NAME)
    SEARCHBASE_NAME = 'dev-search'
    WHOOSH_BASE = os.path.join(basedir, SEARCHBASE_NAME)

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True

class TestinConfig(Config):
    TESTING = True

#class ProductionConfig:
    #TODO

config = {
    'development' : DevelopmentConfig,
    'testing' : TestinConfig,
    #'production' : #TODO

    'default' : DevelopmentConfig
}
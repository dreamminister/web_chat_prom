import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dreamminister'

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
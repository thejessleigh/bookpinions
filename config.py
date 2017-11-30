import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config():
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ['BOOKPINIONS_SECRET']
    SQLALCHEMY_DATABASE_URI = os.environ['BOOKPINIONS_DATABASE_URL']
    REDIS_HOST = 'localhost'
    REDIS_PORT = 6379

class Production(Config):
    DEBUG = False


class DevelopmentConfig(Config):
    DEBUG = True
    DEVELOPMENT = True


class TestingConfig(Config):
    TESTING = True

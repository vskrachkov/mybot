import os

class BaseConfig:
    SECRET_KEY = os.urandom(24)
    APP_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DebugConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://mybot:uberpass@localhost/mybot_db'


class ProdConfig(BaseConfig):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://mybot:zupkaTaktic1034@localhost/mybot_db'

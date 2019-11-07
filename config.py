import os
from dotenv import load_dotenv


basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.flaskenv'))

class Config(object):
    VERSION = '0.0.1'
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'snapekilledumbledore'
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_SUBJECT_PREFIX = os.environ.get('MAIL_SUBJECT_PREFIX')
    ADMIN = os.environ.get('MAIL_SENDER') or 'bryan.bailey@brizzle.dev'
    WTF_CSRF_ENABLED = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or  \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    UPLOAD_FOLDER = os.path.join(basedir, 'app/static/uploads')
    STASH_FOLDER = os.path.join(UPLOAD_FOLDER, 'stash')
    CLOUD_PLATFORM = 'aws'

    @staticmethod
    def init_app(app):
        pass


class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or  \
        'sqlite:///' + os.path.join(basedir, 'dev.db')


class TestConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or  \
        'sqlite:///' + os.path.join(basedir, 'test.db')


# class ProductionConfig(Config):
#     SQLALCHET_BINDS = {
#         'main': SQLALCHEMY_DATABASE_URI
#     }

config = {
    'development': DevConfig,
    'testing': TestConfig,
    'production': Config,
    'default': DevConfig
}
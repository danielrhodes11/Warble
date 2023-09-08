import os


class DevConfig:
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL', 'postgresql:///warbler')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    SECRET_KEY = os.environ.get('SECRET_KEY', "it's a secret")

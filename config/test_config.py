class TestConfig:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "postgresql:///warbler-test"
    SECRET_KEY = "SHHHHHH"
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    SQLALCHEMY_ECHO = False
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

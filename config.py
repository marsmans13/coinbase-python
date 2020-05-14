import os


class Config:
    """Set Flask configuration vars."""

    # General Config
    TESTING = True
    DEBUG = True
    SECRET_KEY = b'_5#y2L"F4Q8z\n\xec]/'
    SESSION_COOKIE_NAME = 'my_cookie'

    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://admin:pleasehackme@1.1.1.1:1738/imamoron'
    SQLALCHEMY_USERNAME = 'admin'
    SQLALCHEMY_PASSWORD = 'pleasehackme'
    SQLALCHEMY_DATABASE_NAME = 'imamoron'
    SQLALCHEMY_TABLE = 'passwords_table'
    SQLALCHEMY_DB_SCHEMA = 'public'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
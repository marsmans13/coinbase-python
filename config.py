import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """Set Flask configuration vars."""

    # General Config
    TESTING = False
    DEBUG = False
    SECRET_KEY = b'_5#y2L"F4Q8z\n\xec]/'
    SESSION_COOKIE_NAME = 'my_cookie'

    # SQLALCHEMY_DATABASE_URI = "postgresql:///coinbase.db"
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(
        user=os.environ['POSTGRES_USER'],
        pw=os.environ['POSTGRES_PW'],
        url=os.environ['POSTGRES_URL'],
        db=os.environ['POSTGRES_DB'])
    SQLALCHEMY_TRACK_MODIFICATIONS = False

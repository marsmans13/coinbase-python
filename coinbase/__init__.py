import os
import sys
import inspect
from flask import Flask
import flask_login
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from config import Config


app = Flask(__name__, instance_relative_config=True)
"APPLICATION CREATED __INIT__"
config = Config()
app.config.from_object(config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from coinbase.auth import auth_bp
from coinbase.markets import market_bp
# from coinbase.models import *


app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(market_bp, url_prefix='/market')

# login_manager = flask_login.LoginManager()
# login_manager.init_app(app)
# login_manager.login_view = 'login'


def create_app(application, test_config=None):

    application.config.from_pyfile('config.py', silent=True)
    print("APPLICATION CONFIGURED FROM FILE")

    connect_to_db(application)
    print("Connected to DB")
    with app.app_context():
        db.create_all()

    return application


def connect_to_db(app, db_uri="postgresql:///coinbase"):
    # app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    # app.config['SQLALCHEMY_ECHO'] = False
    # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # app.config['SECRET_KEY'] = b'_5#y2L"F4Q8z\n\xec]/'
    app.config['CSRF_ENABLED'] = True
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    create_app(app)
    # connect_to_db(app)

    app.run(debug=True)

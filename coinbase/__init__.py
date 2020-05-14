import os
from flask import Flask, Blueprint
from coinbase import db, auth, markets

app = Flask(__name__, instance_relative_config=True)
app.register_blueprint(auth.bp, url_prefix='/auth')
app.register_blueprint(markets.market_bp)
app.config.from_mapping(
    SECRET_KEY='dev',
    DATABASE=os.path.join(app.instance_path, 'coinbase.sqlite')
)

def create_app(test_config=None):
    db.init_app(app)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'coinbase.sqlite'),
    )
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)
    try:
        os.makedirs(app.instance_path)
    except:
        pass
    return app

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DECIMAL
from flask_sqlalchemy import SQLAlchemy
from flask import current_app as app
from coinbase import db


print('KSJDFLKSDNFFJNFJASDNFJKSDANFKJLSDANF')
# with app.app_context():
#     db = SQLAlchemy(app)
print('MODEL APP CREATED')


class User(db.Model):

    __tablename__ = "user"

    id = Column('id', Integer, primary_key=True)
    username = Column('username', String(50))
    email = Column('email', String(50))
    password = Column('password', String(200))
    phone = Column('phone', String(20))

    def __repr__(self):
        return '<User {}>'.format(self.username)


class UserCurrency(db.Model):

    __tablename__ = 'user_currency'
    id = Column('id', Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    currency = Column('currency', String(15))
    amount = Column('amount', DECIMAL(precision=50))


def init_app():
    from flask import Flask

    app = Flask(__name__)
    connect_to_db(app)
    print("Connected to DB")
    return db


def connect_to_db(app, db_uri="postgresql:///coinbase"):
    # app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    # app.config['SQLALCHEMY_ECHO'] = False
    # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # app.config['SECRET_KEY'] = b'_5#y2L"F4Q8z\n\xec]/'
    app.config['CSRF_ENABLED'] = True
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    db.create_all()

import os
from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, BooleanField, SelectField, SubmitField, IntegerField
from wtforms.validators import DataRequired

import coinbasepro as cbp


cb_passphrase = os.environ.get('CB_PASSPHRASE')
cb_public_key = os.environ.get('CB_PUBLIC_KEY')
cb_private_key = os.environ.get('CB_PRIVATE_KEY')


def get_public_client():
    pub_client = cbp.PublicClient()

    return pub_client


def get_auth_client():
    cb_auth = cbp.AuthenticatedClient(
        key=cb_public_key, secret=cb_private_key, passphrase=cb_passphrase
    )

    return cb_auth


def get_currency_list(public_client):
    cur_list = public_client.get_currencies()

    return cur_list


# auth_client = get_auth_client()
# currency_list = get_currency_list(auth_client)

pub_client = cbp.PublicClient()
currency_list = pub_client.get_currencies()


class RegisterForm(FlaskForm):
    username = StringField('Username')
    password = PasswordField('Password')
    email = StringField('Email')
    phone = StringField('Phone')


class AddCurrencyForm(FlaskForm):
    currency = SelectField('Currency', choices=[('', 'Select')] + [(cur['id'], cur['id']) for cur in currency_list])
    submit = SubmitField('Add')


class UpdateAlertForm(FlaskForm):
    currency = SelectField('Currency', choices=[('', 'Select')] + [(cur['id'], cur['id']) for cur in currency_list])
    low_price = IntegerField('Lower threshold')
    high_price = IntegerField('Upper threshold')
    submit = SubmitField("Add Alert")

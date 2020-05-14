from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, BooleanField, SelectField, SubmitField, IntegerField
from wtforms.validators import DataRequired

class AddCurrencyForm(FlaskForm):
    currency = SelectField('Currency', choices=[('BTC-USD', 'BTC-USD'),
                                                ('LTC-USD', 'LTC-USD'),
                                                ('ETH-USD', 'ETH-USD')])
    submit = SubmitField('Add')

class UpdateAlertForm(FlaskForm):
    currency = SelectField('Currency', choices=[('BTC-USD', 'BTC-USD'),
                                                ('LTC-USD', 'LTC-USD'),
                                                ('ETH-USD', 'ETH-USD')])
    low_price = IntegerField('Lower threshold')
    high_price = IntegerField('Upper threshold')
    submit = SubmitField("Add Alert")

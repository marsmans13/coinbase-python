import functools
import os

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
import coinbasepro as cbp
from twilio.rest import Client

from coinbase.forms import AddCurrencyForm, UpdateAlertForm
from coinbase.db import get_db


market_bp = Blueprint('market_bp', __name__)

@market_bp.route('/', methods=['POST', 'GET'])
@market_bp.route('/index', methods=['POST', 'GET'])
def index():
    return redirect(url_for('market_bp.market_index'))

@market_bp.route('/market-index', methods=['POST', 'GET'])
def market_index():
    cb_client = cbp.PublicClient()
    currency = 'BTC-USD'
    response = cb_client.get_product_ticker('BTC-USD')

    form = AddCurrencyForm()
    if form.submit.data:
        currency = form.currency.data
        flash('{} added to your dashboard'.format(currency))

    return render_template('landing.html', currency=currency, response=response, form=form)


account_sid = os.environ.get("SID")
auth_token = os.environ.get("AUTH_TOKEN")
client = Client(account_sid, auth_token)
twilio_from = os.environ.get("TWILIO_FROM")
twilio_to = os.environ.get("TWILIO_TO")


@market_bp.route('/update-alerts', methods=['POST', 'GET'])
def update_alerts():
    form = UpdateAlertForm()
    if form.submit.data:
        if form.high_price.data:
            cur = form.currency.data
            high_message = client.messages.create(
                body="High price alert set for {}".format(cur),
                from_='+12058758151',
                to='+12394045012'
            )
        if form.low_price.data:
            cur = form.currency.data
            low_message = client.messages.create(
                body="Low price alert set for {}".format(cur),
                from_=twilio_from,
                to=twilio_to
            )
        flash("Alert added")
        return redirect(url_for('market_bp.market_index'))
    return render_template("update_alerts.html", form=form)

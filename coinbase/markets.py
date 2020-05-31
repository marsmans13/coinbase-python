import functools
import os

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
import coinbasepro as cbp
from twilio.rest import Client

from coinbase import db
from coinbase.forms import AddCurrencyForm, UpdateAlertForm
from coinbase.auth import get_user, login_required
from coinbase.models import User, UserCurrency


market_bp = Blueprint('market_bp', __name__)

cb_passphrase = os.environ.get('CB_PASSPHRASE')
cb_public_key = os.environ.get('CB_PUBLIC_KEY')
cb_private_key = os.environ.get('CB_PRIVATE_KEY')


@market_bp.route('/', methods=['POST', 'GET'])
@market_bp.route('/index', methods=['POST', 'GET'])
@login_required
def index():
    return redirect(url_for('market_bp.market_index'))


@market_bp.route('/market-index', methods=['POST', 'GET'])
@login_required
def market_index():
    user = get_user(session.get('username'))
    print(user)
    cb_client = cbp.PublicClient()
    user_currencies = UserCurrency.query.filter_by(user_id=user.id).all()

    response = []
    for cur in user_currencies:
        r = cb_client.get_product_ticker(cur.currency)
        response.append((cur.currency, r))

    form = AddCurrencyForm()
    if request.method == 'POST':
        currency = form.currency.data + '-USD'
        new_cur = UserCurrency(user_id=user.id, currency=currency, amount=0.0)
        if new_cur not in user_currencies:
            db.session.add(new_cur)
            db.session.commit()
            flash('{} added to your dashboard'.format(currency))
            return redirect(url_for('market_bp.market_index'))
        else:
            flash('{} already in your dashboard'.format(currency))

    return render_template('landing.html', currency=user_currencies, response=response, form=form)


@market_bp.route('/product-details/<currency_id>', methods=['GET', 'POST'])
@login_required
def get_product_details(currency_id):
    print('CURRENCY ID', currency_id)
    user = get_user(session.get('username'))
    cb_client = cbp.PublicClient()
    cb_auth = cbp.AuthenticatedClient(
        key=cb_public_key, secret=cb_private_key, passphrase=cb_passphrase
    )

    accounts = cb_auth.get_accounts()
    account_id = None
    pub_currency = None

    for acc in accounts:
        if currency_id in acc['currency']:
            account_id = acc['id']
            pub_currency = acc['currency'] + '-USD'
            print('PUB CURRENCY', pub_currency)

    try:
        product_resp = cb_auth.get_account(account_id)
        account_hist = cb_auth.get_account_history(account_id)
        acc_hist = list(account_hist)
        market_resp = cb_client.get_product_ticker(pub_currency)
        fills = cb_auth.get_fills(pub_currency)
        fills_lst = list(fills)
    except:
        return redirect(url_for('market_bp.market_index'))

    if request.method == 'POST':
        currency = pub_currency
        user_currency = UserCurrency.query.filter_by(user_id=user.id).filter_by(currency=currency).first()
        print(user_currency)
        db.session.delete(user_currency)
        db.session.commit()
        flash('{} removed from dashboard'.format(currency))
        return redirect(url_for('market_bp.market_index'))

    return render_template('product_details.html',
                           product=product_resp,
                           market=market_resp,
                           hist=acc_hist,
                           fills=fills_lst)


account_sid = os.environ.get("SID")
auth_token = os.environ.get("AUTH_TOKEN")
client = Client(account_sid, auth_token)
twilio_from = os.environ.get("TWILIO_FROM")
twilio_to = os.environ.get("TWILIO_TO")


@market_bp.route('/update-alerts', methods=['POST', 'GET'])
@login_required
def update_alerts():
    form = UpdateAlertForm()
    if request.method == 'POST':
        if form.high_price.data:
            cur = form.currency.data
            client.messages.create(
                body="High price alert set for {}".format(cur),
                from_=twilio_from,
                to=twilio_to
            )
        if form.low_price.data:
            cur = form.currency.data
            client.messages.create(
                body="Low price alert set for {}".format(cur),
                from_=twilio_from,
                to=twilio_to
            )
        flash("Alert added")
        return redirect(url_for('market_bp.market_index'))
    return render_template("update_alerts.html", form=form)

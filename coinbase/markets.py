import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
import coinbasepro as cbp

from coinbase.db import get_db

bp = Blueprint('market', __name__)

@bp.route('/', methods=['POST', 'GET'])
@bp.route('/index', methods=['POST', 'GET'])
def index():
    return redirect(url_for('market.market_index'))

@bp.route('/market-index', methods=['POST', 'GET'])
def market_index():
    client = cbp.PublicClient()
    currency = 'BTC-USD'
    response = client.get_product_ticker('BTC-USD')

    return render_template('landing.html', currency=currency, response=response)

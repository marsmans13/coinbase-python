import json, hmac, hashlib, time, requests, base64
from requests.auth import AuthBase
import os

import coinbasepro as cbp


# Create custom authentication for Exchange
class CoinbaseExchangeAuth(AuthBase):
    def __init__(self, api_key, secret_key, passphrase):
        self.api_key = api_key
        self.secret_key = secret_key
        self.passphrase = passphrase

    def __call__(self, request):
        timestamp = str(time.time())
        message = (timestamp + request.method + request.path_url + (request.body or '')).encode('UTF-8')
        hmac_key = base64.b64decode(self.secret_key)
        signature = hmac.new(hmac_key, message, hashlib.sha256).digest()
        signature_b64 = base64.b64encode(signature)

        request.headers.update({
            'CB-ACCESS-SIGN': signature_b64,
            'CB-ACCESS-TIMESTAMP': timestamp,
            'CB-ACCESS-KEY': self.api_key,
            'CB-ACCESS-PASSPHRASE': self.passphrase,
            'Content-Type': 'application/json'
        })
        return request

# api_url = 'https://api.pro.coinbase.com/'
# auth = CoinbaseExchangeAuth(os.environ['CB_PUBLIC_KEY'], os.environ['CB_PRIVATE_KEY'], os.environ['CB_PASSPHRASE'])
#
# # Get accounts
# r = requests.get(api_url + 'accounts', auth=auth)
# print(r.json())
# # [{"id": "a1b2c3d4", "balance":...

# Place an order
# order = {
#     'size': 1.0,
#     'price': 1.0,
#     'side': 'buy',
#     'product_id': 'BTC-USD',
# }
# r = requests.post(api_url + 'orders', json=order, auth=auth)
# print(r.json())


cb_passphrase = os.environ.get('CB_PASSPHRASE')
cb_public_key = os.environ.get('CB_PUBLIC_KEY')
cb_private_key = os.environ.get('CB_PRIVATE_KEY')

cb_auth = cbp.AuthenticatedClient(
        key=cb_public_key, secret=cb_private_key, passphrase=cb_passphrase
    )

print(dir(cb_auth))

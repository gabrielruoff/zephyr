import datetime
import json
import logging
import sys
import time

import pandas
import requests

from lib.core import initexit
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(filename='/home/common/dev/logs/zephyr.log', level=logging.DEBUG)

initexithandler = initexit.initexit()
initexithandler.import_dependencies()
# initexithandler.exit()
# time.sleep(1)
# initexithandler.init()
# time.sleep(2)

c = initexithandler.core['LedgerClient'].LedgerClient()
# c._mysql_update('transactions',['value'],['10'],['tx', 'tx'])
# c.do_ledger_transaction('tx', 'rx', '10')
# c._change_balance('1', '10')
asset = 'bnb'
print(c.get_user_id_username(username='test'))
print(c.getbalance('*', username='test'))
# c.do_ledger_transaction(c.get_user_id_username('bank'), c.get_user_id_username('test'), asset, 10)
transactions = {
    'transactions': c.listtransactions(c.get_user_id_username(username='bank'), format=False)
}
print(transactions)
st = c.getselectedticker(c.get_user_id_username(username='bank'))
print(st)
#
default_http_headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
def post(url, method, body, headers=None):
    if headers is None:
        headers = default_http_headers
    data = {'method': method, 'body': body}
    return requests.post(url, data=json.dumps(data), headers=headers).json()
#
# username = 'test'
# method = 'listtransactions'
# body = {
#         'n': '0'
#     }
# transactions = {
#     'table': {
#         'title':
#             'Transactions',
#         'headers':
#             ['Transaction ID', 'Merchant', 'Value', 'New Balance', 'Timestamp'],
#         'transactions':
#             post('http://localhost:5000/Transactions/{}'.format(username), method, body)['data']['transactions']
#     }
# }

# lp = initexithandler.services['LivePrice'].LivePrice()
# assets = ['eth']
# prices = lp.getpriceusd(assets)
# print(prices, float(prices['eth']))
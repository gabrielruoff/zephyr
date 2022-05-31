import datetime
import logging
from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from django.template import loader
import requests
import json
import pandas

logging.basicConfig(filename='/home/common/dev/logs/zephyr.log', level=logging.DEBUG)
default_http_headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}


def index(request, username):
    API_URL = 'https://localhost:5000/{}/{}'
    template = loader.get_template('Account.html')

    method = 'getselectedticker'
    selectedticker = post(API_URL.format('Account', username), method, {})['data']['selectedticker']
    # user data
    user = {
        'username': username,
        'selectedticker': selectedticker,
    }

    # get balances
    method = 'getbalance'
    body = {
        'asset': '*'
    }
    balances = post(API_URL.format('Account', username), method, body)['data']['balance']
    print(balances)

    #  get transactions
    method = 'listtransactions'
    body = {
        'n': '0',
        'format': False,
    }
    transactions = {
        'table': {
            'title':
                'Recent Transactions',
            'headers':
                ['Transaction ID', 'Merchant', 'Asset', 'Value', 'New Balance', 'Timestamp'],
            'transactions':
                reversed(post(API_URL.format('Transactions', username), method, body)['data']['transactions'])
        }
    }
    body['format'] = False
    unformattedtransactions = post(API_URL.format('Transactions', username), method, body)['data']['transactions']
    txtimestamps = sorted([datetime.datetime.strptime(tx[-1], "%m/%d/%Y, %I:%M%p") for tx in unformattedtransactions])
    # print(txtimestamps)
    start = txtimestamps[0]
    end = txtimestamps[-1]
    # print(post('http://localhost:5000/Transactions/{}'.format(username), method, body)['data']['transactions'])
    sortedtransactions = sorttransactionsbyticker(unformattedtransactions)
    # print(sortedtransactions)

    txtimestamps = [{ticker: [datetime.datetime.strptime(tx[-1], "%m/%d/%Y, %I:%M%p") for tx in sortedtransactions[ticker]] for ticker in sortedtransactions}][0]
    # print(txtimestamps)
    # print(start, end)
    labels = [str(d.strftime('%m/%d')) for d in pandas.date_range(start, end, freq='d').union([end])]

    txtimestamps = [{ticker: [txts.strftime('%m/%d') for txts in txtimestamps[ticker]] for ticker in txtimestamps}][0]
    # print(txtimestamps)
    data = [{ticker: [0] * len(labels) for ticker in sortedtransactions}][0]
    # print(data)
    _balance = 0
    maxd = {}
    # print(labels, txtimestamps)
    for ticker in sortedtransactions:
        maxd[ticker] = 0
        # print(ticker+':')
        for i, label in enumerate(labels):
            # print(i, label,':')
            # print(txtimestamps[ticker])
            if label in txtimestamps[ticker]:
                j = max(loc for loc, val in enumerate(txtimestamps[ticker]) if val == label)
                # print(True, j)
                _balance = sortedtransactions[ticker][j][4]
                # print(float(_balance), float(maxd[ticker]))
                if float(_balance) > float(maxd[ticker]):
                    maxd[ticker] = float(_balance)
            data[ticker][i] = float(_balance)
        _balance = 0

    for ticker in sortedtransactions:
        data[ticker] = [100*d/maxd[ticker] for d in data[ticker]]

    # print(labels, data)
    # crypto prices
    method = 'getsupportedtickers'
    tickers = post(API_URL.format('Transactions', username), method, {})['data']['tickers']
    method = 'getpriceusd'
    body = {
        'assets': tickers,
    }
    cryptoprices = post(API_URL.format('Transactions', username), method, body)['data']['prices']

    transactions['balancechart'] = {
        'labels': labels,
        'data': data,
        # 'data2': data2,
    }

    assets = {
        'fiat': {
            'balance': balances.pop('fiat'),
        },
        'crypto': {
            'tickers': tickers,
            'balances': balances,
            'prices': cryptoprices
        }
    }

    context = {
        'user': user,
        'assets': assets,
        'transactions': transactions,
    }
    return HttpResponse(template.render(context, request))


def reload(request, username):
    return index(username)


def post(url, method, body, headers=None):
    if headers is None:
        headers = default_http_headers
    data = {'method': method, 'body': body}
    return requests.post(url, data=json.dumps(data), headers=headers, verify=False).json()

def sorttransactionsbyticker(transactions):
    tx = {}
    for t in transactions:
        try:
            tx[t[2]].append(t)
            pass
        except KeyError as e:
            tx[t[2]] = [t]
    return tx
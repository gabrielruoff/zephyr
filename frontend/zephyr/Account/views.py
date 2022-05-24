import datetime
import logging

from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from django.template import loader
import requests
import json
import pandas

default_http_headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}


def index(request, username):
    API_URL = 'http://localhost:5000/{}/{}'
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
                post(API_URL.format('Transactions', username), method, body)['data']['transactions']
        }
    }
    body['format'] = False
    unformattedtransactions = post(API_URL.format('Transactions', username), method, body)['data']['transactions']
    # print(post('http://localhost:5000/Transactions/{}'.format(username), method, body)['data']['transactions'])
    txtimestamps = [datetime.datetime.strptime(tx[-1], "%m/%d/%Y, %I:%M%p") for tx in unformattedtransactions]
    # print(txtimestamps)
    start = txtimestamps[0]
    end = txtimestamps[-1]
    # print(start, end)
    labels = [str(d.strftime('%m/%d')) for d in pandas.date_range(start, end, freq='d')]
    txtimestamps = [txts.strftime('%m/%d') for txts in txtimestamps]
    data = [0] * len(labels)
    _balance = 0
    print(labels, txtimestamps)
    for i, label in enumerate(labels):
        if label in txtimestamps:
            j = max(loc for loc, val in enumerate(txtimestamps) if val == label)
            _balance = unformattedtransactions[j][4]
            data[i] = _balance
        else:
            data[i] = _balance

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
    return requests.post(url, data=json.dumps(data), headers=headers).json()

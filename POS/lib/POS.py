import json

import requests

from POS.lib import Crypt, HardwareSerial
from dotenv import load_dotenv
import os
import time

load_dotenv('../.env')
_winroot = 'C:/Users/GEruo/Documents/GitHub/zephyr/'
API_URL = 'http://CCR-TESTBENCH:5000/{}/{}'
default_http_headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}


class POS:
    def __init__(self):
        self.identity = None
        self.pkey = os.environ.get('RSA_KEYFILE').replace('/home/common/dev/', _winroot)
        self.keypass = os.environ.get('RSA_KEYPAS')
        self.key = os.environ.get('RSA_KEYFILE').replace('/home/common/dev/', _winroot) + os.environ.get(
            'RSA_PUB_SUFFIX')
        self.arduinoport = 'COM3'


    def __call__(self, **kwargs):
        self.update(kwargs)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def setidentity(self, uid):
        self.identity = {
            'uid': uid,
        }

    def writeuidtocard(self, prompt=True):
        with Crypt.RSACrypt() as crypt:
            uid = int(input('Enter userid to write: '))
            print('encrypting userid')
            crypt.setkey(self.key)
            euid = crypt.encrypt(uid)
        with HardwareSerial.arduino() as arduino:
            arduino.connect(self.arduinoport)
            time.sleep(2)
            input('-- Place the zephyrcard on the payment terminal and press the enter key --')
            arduino.send('w')
            print('writing uid to card...')
            arduino.send(euid)
            done = False
            while not done:
                if arduino.serialport.in_waiting:
                    line = arduino.serialport.readline().decode('utf-8').rstrip('\n')
                    if 'NAK' in line:
                        done = True
                        print('\n')
                    else:
                        print(line)
        if self._verifyuidwrite(uid):
            return '-- Write successful. uid verified: {} --'.format(uid)

    def readuidfromcard(self, prompt=True):
        with HardwareSerial.arduino() as arduino:
            arduino.connect(self.arduinoport)
            time.sleep(2)
            arduino.send('r')
            # if prompt:
                # input('-- Place the zephyrcard on the payment terminal and press the enter key --')
            uid = arduino.receive()
            # print('read enc uid {}'.format(uid))
        with Crypt.RSACrypt() as crypt:
            crypt.setkey(self.pkey, self.keypass)
            uid = crypt.decrypt(uid)
        return uid

    def _verifyuidwrite(self, uid):
        return int(self.readuidfromcard(prompt=False)) == int(uid)

    def sendtransaction(self):
        value = float(input('input the transaction value '))
        uid = self.readuidfromcard()
        selectedticker = getselectedticker(uid)
        priceusd = float(getpriceusd(selectedticker))
        # confirm = input(
        #     'confirm transaction ${:,} ({} {}) [y/n] '.format(float(priceusd * value), str(value), selectedticker))
        # if confirm.upper() == 'Y':
        #     return '\ntransaction successful (txid = {})'.format(dotransaction(uid, *self.identity.values(), value))
        return dotransaction(uid, *self.identity.values(), value)


def post(url, method, body, headers=None):
    if headers is None:
        headers = default_http_headers
    data = {'method': method, 'body': body}
    return requests.post(url, data=json.dumps(data), headers=headers).json()


def getselectedticker(uid):
    method = 'getselectedticker'
    body = {
        'userid': uid,
    }
    return post(API_URL.format('Account', 'null'), method, body)['data']['selectedticker']


def getpriceusd(ticker):
    method = 'getpriceusd'
    body = {
        'assets': [ticker],
    }
    return post(API_URL.format('Transactions', 'null'), method, body)['data']['prices'][ticker]


def dotransaction(txuid, rxuid, value):
    method = 'dotransaction'
    body = {
        'rx': rxuid,
        'value': value,
        'txuserid': txuid,
    }
    return post(API_URL.format('Transactions', 'null'), method, body)['data']


# print('-- Zephyr POS --')
# options = {
#     '1': {
#         'method': 'writeuidtocard',
#         'description': 'Write a userid to a Zephyrcard'
#     },
#     '2': {
#         'method': 'readuidfromcard',
#         'description': 'Read a userid from a Zephyrcard'
#     },
#     '3': {
#         'method': 'sendtransaction',
#         'description': 'Process a transaction'
#     },
# }
#
# selected = input(
#     'options\n' + str(
#         '\n'.join(['{} - {}'.format(option, options[option]['description']) for option in options]) + '\n'))
#
# identity = [2, '23456']
# pos = POS(*identity)
# func = getattr(pos, options[selected]['method'])
# print(func())

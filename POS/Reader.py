from lib import Crypt, HardwareSerial
import requests
from dotenv import load_dotenv
import json
import time
import os

load_dotenv('../.env')
_winroot = 'C:/Users/GEruo/Documents/GitHub/zephyr/'
API_URL = 'http://localhost:5000/pos/{}'
default_http_headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
pkey = os.environ.get('RSA_KEYFILE').replace('/home/common/dev/', _winroot)
keypass = os.environ.get('RSA_KEYPAS')


def insertreaderdata(uid):
    method = 'insertreaderdata'
    return post(API_URL.format(uid), method, {})['data']


def post(url, method, body, headers=None):
    if headers is None:
        headers = default_http_headers
    data = {'method': method, 'body': body}
    return requests.post(url, data=json.dumps(data), headers=headers).json()


arduino = HardwareSerial.arduino()
arduino.connect('COM3')
time.sleep(2)
while True:
    arduino.send('r')
    print('sent r')
    print('waiting to receive')
    uid = arduino.receive()
    print('raw uid {}'.format(repr(uid)))
    with Crypt.RSACrypt() as crypt:
        crypt.setkey(pkey, keypass)
        uid = crypt.decrypt(uid)
        print('received {}'.format(uid))
    insertreaderdata(uid)
    print('inserted')
    time.sleep(2)
# Import libraries
import json
import requests
import os
from dotenv import load_dotenv
import sys
import logging

sys.path.insert(1, os.environ.get('PATH_ETHEREUM'))

logging.basicConfig(filename='/home/common/dev/logs/zephyr.log', level=logging.DEBUG)
load_dotenv('/home/common/dev/.env')

class LivePrice:
    def __init__(self):
        self.baseurl = 'https://api.binance.com/api/v3/ticker/price?symbol={}USDT'
    def __enter__(self):
        self.__init__()
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def getpriceusd(self, assets):
        prices = {}
        for asset in assets:
            data = requests.get(self.baseurl.format(asset.upper()))
            data = data.json()
            prices[asset] = data['price']
        return prices
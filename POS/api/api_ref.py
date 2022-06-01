from flask import Flask
from flask_restful import Api, Resource, request
import logging
import sqlite3
from POS.lib import POS, LivePrice


# logging.basicConfig(filename='/home/common/dev/logs/zephyr.log', level=logging.DEBUG)
import requests

class pos:
    def __init__(self):
        pass

    def __enter__(self):
        self.__init__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def uidfromcard(self, uid, body):
        with POS.POS() as p:
            p.setidentity(uid)
            uid = p.readuidfromcard()
            return build_api_response(True, data=uid, wrapper='uid')

    def dotransaction(self, uid, body):
        return POS.dotransaction(uid, body['rxuid'], body['value'])

    def getselectedticker(self, uid, body):
        ticker = POS.getselectedticker(uid)
        return build_api_response(True, data=ticker, wrapper='ticker')

    def insertreaderdata(self, uid, body):
        with sqlite3.connect('pos.db') as conn:
            cur = conn.cursor()
            cur.execute("UPDATE pos SET read=? where true", (uid))
        return build_api_response(True)

    def retrievereaderdata(self, uid, body):
        with sqlite3.connect('pos.db') as conn:
            cur = conn.cursor()
            cur.execute("select read from pos")
            data = cur.fetchall()[0][0]
            cur.close()
            self.clearreaderdata(uid, body)
            return build_api_response(True, data=data, wrapper='read')

    def clearreaderdata(self, uid, body):
        self.insertreaderdata('0', None)
        return build_api_response(True)




class data:
    def __init__(self):
        pass

    def __enter__(self):
        self.__init__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def getpriceusd(self, body):
        print(body)
        with LivePrice.LivePrice() as lp:
            prices = lp.getpriceusd(body['assets'])
            print(prices)
            return build_api_response(True, data=prices, wrapper='prices')


    # def pricelookup(self, uid, body):
    #     selectedticker = POS.getselectedticker(uid)
    #     priceusd = float(POS.getpriceusd(selectedticker))
    #     return build_api_response(True, data=priceusd, wrapper='priceusd')


def build_api_response(success, err='', data='', wrapper=''):
    if wrapper:
        return {'success': success, 'data': {wrapper: data}, 'err': err}
    return {'success': success, 'data': data, 'err': err}


def _islocalorigin(addr):
    localaddresses = ['127.0.0.1', 'localhost']
    if addr in localaddresses:
        return True
    return False

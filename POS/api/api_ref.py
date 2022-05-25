from flask import Flask
from flask_restful import Api, Resource, request
import logging
from POS.lib import POS


# logging.basicConfig(filename='/home/common/dev/logs/zephyr.log', level=logging.DEBUG)


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
            print(uid)
            return build_api_response(True, data=uid, wrapper='uid')

    # def pricelookup(self, uid, body):
    #     selectedticker = POS.getselectedticker(uid)
    #     priceusd = float(POS.getpriceusd(selectedticker))
    #     return build_api_response(True, data=priceusd, wrapper='priceusd')

    def dotransaction(self, uid, body):
        return POS.dotransaction(uid, body['rxuid'], body['value'])


def build_api_response(success, err='', data='', wrapper=''):
    if wrapper:
        return {'success': success, 'data': {wrapper: data}, 'err': err}
    return {'success': success, 'data': data, 'err': err}


def _islocalorigin(addr):
    localaddresses = ['127.0.0.1', 'localhost']
    if addr in localaddresses:
        return True
    return False

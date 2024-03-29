from flask import Flask
from flask_restful import Api, Resource, request
import logging
from lib.core import initexit

logging.basicConfig(filename='/home/common/dev/logs/zephyr.log', level=logging.DEBUG)


class accounts:
    def __init__(self):
        self.initexithandler = initexit.initexit()
        self.initexithandler.import_dependencies()
        self.core = self.initexithandler.dependencies['core']

    def __enter__(self):
        self.__init__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def getbalance(self, username, body):
        asset = body['asset']
        logging.debug('[API] retrieving {} balance for {}'.format(asset, username))
        with self.initexithandler.core['LedgerClient'].LedgerClient() as ledger:
            balance = ledger.getbalance(asset, username=username)
            logging.debug('[API] found {} balance {} for {}'.format(asset, balance, username))
            return build_api_response(True, data=balance, wrapper='balance')

    def setselectedticker(self, username, body):
        with self.initexithandler.core['LedgerClient'].LedgerClient() as ledger:
            try:
                uid = body['userid']
            except KeyError as e:
                uid = ledger.get_user_id_username(username=username)
            if ledger.setselectedticker(uid, body['selectedticker']):
                return build_api_response(True)

    def getselectedticker(self, username, body):
        with self.initexithandler.core['LedgerClient'].LedgerClient() as ledger:
            try:
                uid = body['userid']
            except KeyError as e:
                uid = ledger.get_user_id_username(username=username)
            st = ledger.getselectedticker(uid)
            return build_api_response(True, data=st, wrapper='selectedticker')


class transactions:
    def __init__(self):
        self.initexithandler = initexit.initexit()
        self.initexithandler.import_dependencies()

    def __enter__(self):
        self.__init__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    # tx and rx are in username format
    def dotransaction(self, username, body):
        rxuid = body['rx']
        value = body['value']
        # pkey = body['pkey']
        with self.initexithandler.core['LedgerClient'].LedgerClient() as ledger:
            try:
                txuid = body['txuserid']
            except KeyError as e:
                txuid = ledger.get_user_id_username(username=username)
            asset = ledger.getselectedticker(txuid)
            logging.debug('[API] attempting {} transaction {} -> {} ({})'.format(asset, txuid, rxuid, str(value)))
            ledger.do_ledger_transaction(txuid, rxuid, asset, value)
            tx_id = ledger.get_latest_transaction_id(txuid)
            logging.debug('[API] transaction successful')
            return build_api_response(True, data=tx_id, wrapper='tx_id')

    def listtransactions(self, username, body):
        n = body['n']
        format = body['format']
        logging.debug('[API] attempting to retrieve {} transactions for user \'{}\''.format(int(n), str(username)))
        try:
            pkey = body['pkey']
        except KeyError as e:
            logging.debug('[API] pkey omitted')
        with self.initexithandler.core['LedgerClient'].LedgerClient() as ledger:
            uid = ledger.get_user_id_username(username)
            if not _islocalorigin(body['origin']):
                logging.debug('[API] trying submitted pkey {}'.format(pkey))
                if ledger.verify_pkey(uid, pkey):
                    logging.debug('[API] pkey accepted, proceeding')
                else:
                    logging.debug('[API] pkey rejected, cancelling')
                    return build_api_response(False, err='invalid pkey')
            else:
                logging.debug('[API] request orign is local, proceeding')

            logging.debug('[API] retrieving transactions')
        return build_api_response(True, data=ledger.listtransactions(uid, int(n), format=format),
                                  wrapper='transactions')

    def getpriceusd(self, username, body):
        with self.initexithandler.services['LivePrice'].LivePrice() as liveprice:
            prices = liveprice.getpriceusd(body['assets'])
            return build_api_response(True, data=prices, wrapper='prices')

    def getsupportedtickers(self, username, body):
        with self.initexithandler.core['LedgerClient'].LedgerClient() as ledger:
            tickers = ledger.getsupportedtickers()
            tickers.remove('fiat')
            return build_api_response(True, data=tickers, wrapper='tickers')


def build_api_response(success, err='', data='', wrapper=''):
    if wrapper:
        return {'success': success, 'data': {wrapper: data}, 'err': err}
    return {'success': success, 'data': data, 'err': err}


def _islocalorigin(addr):
    localaddresses = ['127.0.0.1', 'localhost']
    if addr in localaddresses:
        return True
    return False

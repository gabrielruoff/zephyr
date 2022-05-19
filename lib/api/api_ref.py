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


class transactions:
    def __init__(self):
        self.initexithandler = initexit.initexit()
        self.initexithandler.import_dependencies()
        self.core = self.initexithandler.dependencies['core']

    def __enter__(self):
        self.__init__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    # tx and rx are in username format
    def do_transaction(self, tx, rx, value, pkey):
        logging.debug('[API] attempting transaction {} -> {} ({})'.format(tx, rx, str(value)))
        with self.core['LedgerClient'].LedgerClient() as ledger:
            txuid = ledger._get_user_id_from_username(tx)
            rxuid = ledger._get_user_id_from_username(rx)
            # verify pkey
            logging.debug('[API] trying submitted pkey {}'.format(pkey))
            if ledger.verify_pkey(txuid, pkey):
                logging.debug('[API] pkey accepted, proceeding')
                ledger.do_ledger_transaction(txuid, rxuid, value)
                tx_id = ledger._get_latest_transaction_id(txuid)
            else:
                logging.debug('[API] pkey rejected, cancelling transaction')
                return False
            logging.debug('[API] transaction successful')
            return tx_id

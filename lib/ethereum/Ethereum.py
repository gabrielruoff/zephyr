from web3 import Web3
import os
from dotenv import load_dotenv
import logging

load_dotenv('/home/common/dev/.env')


class Ethereum:
    def __init__(self):
        self.connection_string = 'http://{}:{}'.format(os.environ.get('GANACHE_HOST'), os.environ.get('GANACHE_PORT'))
        logging.debug('trying Web3 provider {}'.format(self.connection_string))
        self.w3 = Web3(Web3.HTTPProvider(self.connection_string))
        if not self.w3.isConnected():
            raise Warning('Web3 client could not connect')
        else:
            logging.debug('Web3 client connected to {}'.format(self.connection_string))
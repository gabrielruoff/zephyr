import sys
from web3 import Web3
import os
from dotenv import load_dotenv
import logging
import json

load_dotenv('/home/common/dev/.env')
logging.basicConfig(filename='/home/common/dev/logs/zephyr.log', level=logging.DEBUG)
sys.path.insert(1, os.environ.get('PATH_SERVICES'))
from Ganache import Ganache


class Ethereum:
    def __init__(self):
        # make sure ganache is running
        with Ganache() as g:
            if not g._detect_running():
                raise Warning('Cannot initialize Ethereum.py. Ganache is not running')
        self.connection_string = 'http://{}:{}'.format(os.environ.get('GANACHE_HOST'), os.environ.get('GANACHE_PORT'))
        logging.debug('trying Web3 provider {}'.format(self.connection_string))
        self.w3 = Web3(Web3.HTTPProvider(self.connection_string))
        if not self.w3.isConnected():
            raise Warning('Web3 client could not connect')
        else:
            logging.debug('Web3 client connected to {}'.format(self.connection_string))
        self.keys = os.environ.get('GANACHE_KEYSPATH')
        self.addresses = self._get_addresses()
        self.rootaddress = self.addresses[0]
        self.rootkey = self._get_privkey(self.rootaddress)

    def __enter__(self):
        self.__init__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def _get_addresses(self):
        _addresses = []
        with open(self.keys, 'r') as k:
            _keys = json.loads(k.read())
        for a in iter(_keys['addresses']):
            _addresses.append(a)
        return _addresses

    def _get_balance(self, address):
        return self.w3.eth.getBalance(Web3.toChecksumAddress(address))

    def _get_privkey(self, address):
        with open(self.keys, 'r') as k:
            _keys = json.loads(k.read())
        _privkey = _keys['addresses'][address]['secretKey']['data']
        return bytes(_privkey)

    def do_transaction(self, tx, rx, value):
        logging.debug('Trying transaction {} -> {} ({} ether)'.format(tx, rx, value))
        try:
            _rx = Web3.toChecksumAddress(rx)
            _tx = Web3.toChecksumAddress(tx)
            _nonce = self.w3.eth.getTransactionCount(_tx)
            _transaction = {
                'nonce': _nonce,
                'to': _rx,
                'value': Web3.toWei(value, 'ether'),
                'gasPrice': 20000000000,
                'gas': 4712388
            }
            logging.debug('Building transaction {}'.format(_transaction))
            _transaction = self.w3.eth.account.signTransaction(_transaction, self._get_privkey(tx))
            logging.debug('Signed Transaction')
            tx_hash = self.w3.eth.sendRawTransaction(_transaction.rawTransaction)
            logging.debug('Transaction success ({})'.format(tx_hash))
            return Web3.toHex(tx_hash)
        except Exception as e:
            logging.debug('Transaction failed: {}'.format(e))

# e = Ethereum()
# print(e.rootkey)
# print(e.getbalance(e.addresses[1]))
# print(e.getbalance(e.addresses[0]))
# print(bytes(e.rootkey))
# print(e.addresses[0])
# e.transaction(e.addresses[0], e.addresses[1], 10)
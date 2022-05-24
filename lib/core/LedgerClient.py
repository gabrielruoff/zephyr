import logging
import os
import sys
from decimal import Decimal

import mysql.connector
from dotenv import load_dotenv

sys.path.insert(1, os.environ.get('PATH_SERVICES'))
from Ethereum import Ethereum
from LivePrice import LivePrice

logging.basicConfig(filename='/home/common/dev/logs/zephyr.log', level=logging.DEBUG)
load_dotenv('/home/common/dev/.env')


class LedgerClient:
    def __init__(self):
        self.host = os.environ.get('LEDGER_HOST')
        self.user = os.environ.get('LEDGER_USER')
        self.passwd = os.environ.get('LEDGER_PASS')
        self.port = os.environ.get('LEDGER_PORT')
        self.db = os.environ.get('LEDGER_DB')
        self.cnx = mysql.connector.connect(user=self.user, password=self.passwd, host=self.host, port=self.port,
                                           database=self.db)

        self._userstable = 'users'
        self._transactionstable = 'transactions'

    def __enter__(self):
        self.__init__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def do_deposit(self, rx, value):
        pass

    def do_withdrawl(self, rx, value):
        logging.debug('Trying withdrawl: {} ether to {}'.format(value, rx))
        with Ethereum() as e:
            tx_hash = e.do_transaction(e.rootaddress, rx, value)
            if tx_hash:
                logging.debug('Eth withdrawl success')
                rx_balance = self.getbalance(user_id=rx)
                self._change_balance(rx, rx_balance - value)
                return True
            else:
                logging.debug('Eth withdrawl failed')
                return False

    # tx and rx are in user_id format
    def do_ledger_transaction(self, tx, rx, asset, value):
        # get user balances and calculate new balances
        # 0 is tx 1 is rx
        balances = (float(self.getbalance(asset, user_id=tx)[asset]), float(self.getbalance(asset, user_id=rx)[asset]))
        nb = [str(balances[0] - float(value)), str(balances[1] + float(value))]
        _fields = ['tx', 'rx', 'asset', 'value', 'nbtx', 'nbrx']
        _values = [str(tx), str(rx), str(asset), str(value), *nb]
        # insert transaction into transactions table
        self._mysql_insert(self._transactionstable, _fields, _values)
        # update user balances in users table
        self._change_balance(tx, asset, nb[0])
        self._change_balance(rx, asset, nb[1])
        return True

    def listtransactions(self, user_id, n=0, format=True):
        # transactions where user_id is tx
        rstx = self._mysql_select(self._transactionstable, 'tx', user_id, selection='PK_transaction_id, rx, asset, value, nbtx, timestamp')
        # transactions where user_id is rx
        rsrx = self._mysql_select(self._transactionstable, 'rx', user_id, selection='PK_transaction_id, tx, asset, value, nbrx, timestamp')
        rs = [*self._formattransactionslist(user_id, rstx, format=format), *self._formattransactionslist(user_id, rsrx, format=format)]
        if n != 0:
            return rs[0:n]
        return rs

    def get_user_id_username(self, username=None, user_id=None):
        if username is not None:
            match = ['username', username]
            selection = 'PK_user_id'
        if user_id is not None:
            match = ['PK_user_id', user_id]
            selection = 'username'
        rs = self._mysql_select(self._userstable, *match, selection=selection)
        return str(rs[0][0])

    def verify_pkey(self, user_id, pkey):
        return str(pkey) == self._get_pkey_from_user_id(user_id)

    def setselectedticker(self, user_id, ticker):
        fields = ['selected']
        where = ['PK_user_id', user_id]
        self._mysql_update(self._userstable, fields, [ticker], where)
        return True

    def getselectedticker(self, user_id):
        match = ['PK_user_id', user_id]
        st = self._mysql_select(self._userstable, *match, selection='selected')
        return str(st[0][0])

    def _change_balance(self, user_id, asset, newbalance):
        logging.debug('Changing balance for {} to {}'.format(user_id, newbalance))
        _fields = ['{}balance'.format(asset)]
        _data = [newbalance]
        _where = ['PK_user_id', user_id]
        try:
            self._mysql_update(self._userstable, _fields, _data, _where)
            logging.debug('Change balance succeeded ({} -> {})'.format(user_id, newbalance))
            return True
        except Exception as e:
            logging.debug('Change balance failed ({})'.format(e))
            return False

    def _get_pkey_from_user_id(self, user_id):
        rs = self._mysql_select(self._userstable, 'PK_user_id', user_id, selection='pkey')
        return str(rs[0][0])

    def get_latest_transaction_id(self, user_id):
        txid = self._mysql_select(self._transactionstable, 'tx', user_id, suffix='order by PK_transaction_id desc', selection='PK_transaction_id')
        return str(txid[0][0])

    def getbalance(self, asset, username='', user_id='', update=True):
        assets = [asset]
        balances = {}
        s = ''
        f = 'PK_user_id'
        if username:
            s = self.get_user_id_username(username=username)
        elif user_id:
            s = user_id
        if update:
            self._updatefiatbalance(s)
        if asset == '*':
            assets = self.getsupportedtickers()
        for a in assets:
            ai = a
            balances[ai] = float(self._mysql_select(self._userstable, f, s, selection='{}balance'.format(a))[0][0])
        return balances

    def getsupportedtickers(self):
        tickers = self._mysql_select('INFORMATION_SCHEMA.COLUMNS', 'TABLE_NAME', 'users', suffix=
            ' and COLUMNS.COLUMN_NAME LIKE \'%balance\'', selection='COLUMNS.COLUMN_NAME', db='')
        return [ticker[0].split('balance')[0] for ticker in tickers]

    def _updatefiatbalance(self, user_id):
        fiatbalance = 0
        cryptotickers = self.getsupportedtickers()
        cryptobalances = self.getbalance('*', user_id=user_id, update=False)
        del cryptobalances['fiat']
        cryptotickers = [b.split('balance')[0] for b in cryptotickers]
        cryptotickers.remove('fiat')
        with LivePrice() as liveprice:
            cryptoprices = liveprice.getpriceusd(cryptobalances)
        for ticker in cryptotickers:
            fiatbalance += float(cryptobalances[ticker]) * float(cryptoprices[ticker])
        self._mysql_update(self._userstable, ['fiatbalance'], [fiatbalance], ['PK_user_id', user_id])

    def _formattransactionslist(self, user_id, txlist, format=True):
        if format:
            return [[tx[0], self.get_user_id_username(user_id=user_id), tx[2], '-${:,}'.format(Decimal(tx[3])), '+${:,}'.format(Decimal(tx[4])), *tx[5:-1], tx[-1].strftime("%m/%d/%Y, %I:%M%p")] for tx in txlist]
        return [[tx[0], self.get_user_id_username(user_id=user_id), tx[2], '{}'.format(Decimal(tx[3])), '{}'.format(Decimal(tx[4])), *tx[5:-1], tx[-1].strftime("%m/%d/%Y, %I:%M%p")] for tx in txlist]

    def _mysql_select(self, table, match_field, match_target, suffix='', selection='*', db=None):
        if db is None:
            db = self.db + '.'
        elif db != '':
            db += '.'
        q = 'SELECT {} FROM {} WHERE {}=\'{}\'' + suffix
        d = (selection, (db + table), match_field, match_target)
        # print(q.format(*d))
        cursor = self.cnx.cursor()
        cursor.execute(q.format(*d))
        selected = cursor.fetchall()
        cursor.close()
        return selected

    def _mysql_insert(self, table, fields, data, suffix=""):
        fields = [field.replace('\'', '\\''') for field in fields]
        data = [d.replace('\'', '\\''') for d in data]
        q = "INSERT INTO %s (" + ("%s, " * (len(fields) - 1)) + "%s) VALUES (" + (
                "'%s', " * (len(data) - 1)) + "'%s') " + suffix
        d = (self.db + '.' + table, *fields, *data)
        # print(q % d)
        cursor = self.cnx.cursor()
        cursor.execute(q % d)
        self.cnx.commit()
        cursor.close()
        return True

    def _mysql_update(self, table, fields, data, where, suffix=''):
        q = "UPDATE %s SET " + (("%s='%s', " * (len(fields) - 1)) + "%s='%s'") + " WHERE %s='%s'" + suffix
        # list to store ordered field=data information for set clause
        fieldsdata = []
        while fields:
            fieldsdata.append(fields.pop(0))
            fieldsdata.append(data.pop(0))
        d = (self.db + '.' + table, *fieldsdata, *where)
        cursor = self.cnx.cursor()
        # print(q % d)
        cursor.execute(q % d)
        self.cnx.commit()
        cursor.close()
        return True

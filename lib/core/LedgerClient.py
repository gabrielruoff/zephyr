import logging
import os
import sys

import mysql.connector
from dotenv import load_dotenv

sys.path.insert(1, os.environ.get('PATH_ETHEREUM'))
from Ethereum import Ethereum

logging.basicConfig(filename='/home/common/dev/logs/zephyr.log', level=logging.DEBUG)
load_dotenv('/home/common/dev/.env')


class LedgerClient:
    def __init__(self):
        self.host = os.environ.get('LEDGER_HOST')
        self.user = os.environ.get('LEDGER_USER')
        self.passwd = os.environ.get('LEDGER_PASS')
        self.port = os.environ.get('LEDGER_PORT')
        self.db = os.environ.get('LEDGER_DB')
        self.cnx = mysql.connector.connect(user=self.user, password=self.passwd, host=self.host, port=self.port, database=self.db)

        self._userstable = 'users'
        self._transactionstable = 'transactions'

    def do_deposit(self, rx, value):
        pass

    def do_withdrawl(self, rx, value):
        logging.debug('Trying withdrawl: {} ether to {}'.format(value, rx))
        with Ethereum() as e:
            tx_hash = e.do_transaction(e.rootaddress, rx, value)
            if tx_hash:
                logging.debug('Eth withdrawl success')
                rx_balance = self._get_balance(user_id=rx)
                self._change_balance(rx, rx_balance - value)
                return True
            else:
                logging.debug('Eth withdrawl failed')
                return False

    def do_ledger_transaction(self, tx, rx, value):
        _fields = ['tx', 'rx', 'value']
        _values = [str(tx), str(rx), str(value)]
        # process transaction on ledger
        self._mysql_insert(self._transactionstable, _fields, _values)
        # update user balances accordingly
        tx_balance = self._get_balance(user_id=tx)
        rx_balance = self._get_balance(user_id=rx)
        self._change_balance(tx, tx_balance - value)
        self._change_balance(rx, rx_balance + value)
        return True

    def _change_balance(self, user_id, newbalance):
        logging.debug('Changing balance for {} to {}'.format(user_id, newbalance))
        _fields = ['balance']
        _data = [newbalance]
        _where = ['PK_user_id', user_id]
        try:
            self._mysql_update(self._userstable, _fields, _data, _where)
            logging.debug('Change balance succeeded ({} -> {})'.format(user_id, newbalance))
            return True
        except Exception as e:
            logging.debug('Change balance failed ({})'.format(e))
            return False

    def _get_user_id_from_username(self, username):
        rs = self._mysql_select(self._userstable, 'username', username, selection='PK_user_id')
        return int(rs[0][0])

    def _get_balance(self, username='', user_id=''):
        s = ''
        f = ''
        if username:
            s = username
            f = 'username'
        elif user_id:
            s = user_id
            f = 'PK_user_id'
        rs = self._mysql_select(self._userstable, f, s, selection='balance')
        return float(rs[0][0])

    def _mysql_select(self, table, match_field, match_target, suffix='', selection='*'):
        q = "SELECT %s FROM %s WHERE %s='%s'" + suffix
        d = (selection, (self.db + '.' + table), match_field, match_target)
        # print(q % d)
        cursor = self.cnx.cursor()
        cursor.execute(q % d)
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

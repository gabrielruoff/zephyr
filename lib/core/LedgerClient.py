import logging
import os
import sys

import mysql.connector
from dotenv import load_dotenv

sys.path.insert(1, os.environ.get('PATH_ETHEREUM'))
from Ethreum import Ethereum

logging.basicConfig(filename='/home/common/dev/logs/zephyr.log', level=logging.DEBUG)
load_dotenv('/home/common/dev/.env')


class LedgerClient:
    def __init__(self):
        self.host = os.environ.get('LEDGER_HOST')
        self.user = os.environ.get('LEDGER_USER')
        self.passwd = os.environ.get('LEDGER_PASS')
        self.port = os.environ.get('LEDGER_PORT')
        self.db = os.environ.get('LEDGER_DB')
        self.cnx = mysql.connector.connect(user=self.user, password=self.passwd, host=self.host, database=self.db)

    def do_deposit(self, rx, value):
        pass

    def do_withdrawl(self, rx, value):
        logging.debug('Trying withdrawl: {} ether to {}'.format(value, rx))
        with Ethereum() as e:
            tx_hash = e.do_transaction(e.rootaddress, rx, value)
            if tx_hash:
                logging.debug('Withdrawl success')
                return True
            else:
                logging.debug('Withdrawl failed')
                return False

    def do_ledger_transaction(self, tx, rx):
        pass

    def _ledger_select(self, cnx, db, table, match_field, match_target, suffix='', selection='*'):
        q = "SELECT %s FROM %s WHERE %s='%s'" + suffix
        d = (selection, (db + '.' + table), match_field, match_target)
        # print(q % d)
        cursor = cnx.cursor()
        cursor.execute(q % d)
        selected = cursor.fetchall()
        cursor.close()
        return selected

    def _ledger_insert(self, cnx, db, table, fields, data, user, password, host, suffix=""):
        fields = [field.replace('\'', '\\''') for field in fields]
        data = [d.replace('\'', '\\''') for d in data]
        q = "INSERT INTO %s (" + ("%s, " * (len(fields) - 1)) + "%s) VALUES (" + (
                "'%s', " * (len(data) - 1)) + "'%s') " + suffix
        d = (db + '.' + table, *fields, *data)
        # print(q % d)
        cursor = cnx.cursor()
        cursor.execute(q % d)
        cnx.commit()
        cursor.close()
        return True

    def _ledger_update(self, cnx, db, table, fields, data, where, target, suffix=''):
        q = "UPDATE %s SET " + (("%s='%s', " * (len(fields) - 1)) + "%s='%s'") + " WHERE %s='%s'" + suffix
        # list to store ordered field=data information for set clause
        fieldsdata = []
        while fields:
            fieldsdata.append(fields.pop(0))
            fieldsdata.append(data.pop(0))
        d = (db+ '.' + table, *fieldsdata, where, target)
        cursor = cnx.cursor()
        print(q % d)
        cursor.execute(q % d)
        cnx.commit()
        updated = cursor.fetchall()
        cursor.close()
        return True


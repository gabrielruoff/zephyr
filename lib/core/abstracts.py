import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv('/home/common/dev/.env')


class ledger:
    def __init__(self):
        # database definition
        self.tables = ['users', 'balances', 'transactions']

        self.host = os.environ.get('LEDGER_HOST')
        self.user = os.environ.get('LEDGER_USER')
        self.passwd = os.environ.get('LEDGER_PASS')
        self.port = os.environ.get('LEDGER_PORT')
        self.db = os.environ.get('LEDGER_DB')
        _connectionstring = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(self.user, self.passwd, self.host, self.port, self.db)
        self.cnxengine = create_engine(_connectionstring)
        self.ledger = {}
        self.ledger_pd = {}
        self._import_tables()

    def _import_tables(self):
        # for each table in definition
        for table in self.tables:
            # initialize key in dict
            self.ledger[table] = {}
            # read table from database
            self.ledger_pd[table] = pd.read_sql('SELECT * FROM {}.{}'.format(self.db, table), con=self.cnxengine)
            # format into dict
            for column in self.ledger_pd[table]:
                self.ledger[table][column] = self.ledger_pd[table][column].values.tolist()

l = ledger()
print(l.ledger)
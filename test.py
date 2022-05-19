import logging
import sys
import time

from lib.core import initexit
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(filename='/home/common/dev/logs/zephyr.log', level=logging.DEBUG)

initexithandler = initexit.initexit()
initexithandler.import_dependencies()
# initexithandler.exit()
# time.sleep(1)
# initexithandler.init()
# time.sleep(2)

c = initexithandler.core['LedgerClient'].LedgerClient()
# c._mysql_update('transactions',['value'],['10'],['tx', 'tx'])
# c.do_ledger_transaction('tx', 'rx', '10')
# c._change_balance('1', '10')
print(c._get_user_id_from_username('test'))
print(c._get_balance(username='test'))
c.do_ledger_transaction(c._get_user_id_from_username('bank'), c._get_user_id_from_username('test'), 10)
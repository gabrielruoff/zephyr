import logging

import pandas as pd

from lib.core import initexit
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
logging.basicConfig(filename='/home/common/dev/logs/zephyr.log', level=logging.DEBUG)

initexithandler = initexit.initexit()
initexithandler.import_dependencies()
initexithandler.init()

sqldata = [{"PK_transaction_id":1,"tx":1,"rx":2,"asset":"eth","value":0.20,"timestamp":"02/17/22"},
{"PK_transaction_id":2,"tx":1,"rx":2,"asset":"eth","value":0.18,"timestamp":"02/18/22"},
{"PK_transaction_id":3,"tx":1,"rx":2,"asset":"btc","value":-0.08,"timestamp":"02/19/22"},
{"PK_transaction_id":4,"tx":1,"rx":2,"asset":"btc","value":-0.01,"timestamp":"02/20/22"},
{"PK_transaction_id":5,"tx":1,"rx":2,"asset":"eth","value":0.13,"timestamp":"02/21/22"},
{"PK_transaction_id":6,"tx":1,"rx":2,"asset":"bnb","value":-0.09,"timestamp":"02/22/22"},
{"PK_transaction_id":7,"tx":1,"rx":2,"asset":"bnb","value":-0.15,"timestamp":"02/23/22"},
{"PK_transaction_id":8,"tx":1,"rx":2,"asset":"btc","value":-0.03,"timestamp":"02/24/22"},
{"PK_transaction_id":9,"tx":1,"rx":2,"asset":"bnb","value":0.11,"timestamp":"02/25/22"},
{"PK_transaction_id":10,"tx":1,"rx":2,"asset":"btc","value":0.02,"timestamp":"02/26/22"},
{"PK_transaction_id":11,"tx":1,"rx":2,"asset":"btc","value":0.14,"timestamp":"02/27/22"},
{"PK_transaction_id":12,"tx":1,"rx":2,"asset":"bnb","value":-0.04,"timestamp":"02/28/22"},
{"PK_transaction_id":13,"tx":1,"rx":2,"asset":"bnb","value":0.07,"timestamp":"03/01/22"},
{"PK_transaction_id":14,"tx":1,"rx":2,"asset":"bnb","value":-0.06,"timestamp":"03/02/22"},
{"PK_transaction_id":15,"tx":1,"rx":2,"asset":"bnb","value":0.18,"timestamp":"03/03/22"},
{"PK_transaction_id":16,"tx":1,"rx":2,"asset":"btc","value":-0.17,"timestamp":"03/04/22"},
{"PK_transaction_id":17,"tx":1,"rx":2,"asset":"btc","value":-0.06,"timestamp":"03/05/22"},
{"PK_transaction_id":18,"tx":1,"rx":2,"asset":"bnb","value":0.06,"timestamp":"03/06/22"},
{"PK_transaction_id":19,"tx":1,"rx":2,"asset":"eth","value":-0.01,"timestamp":"03/07/22"},
{"PK_transaction_id":20,"tx":1,"rx":2,"asset":"bnb","value":0.04,"timestamp":"03/08/22"},
{"PK_transaction_id":21,"tx":1,"rx":2,"asset":"eth","value":0.15,"timestamp":"03/09/22"},
{"PK_transaction_id":22,"tx":1,"rx":2,"asset":"btc","value":0.10,"timestamp":"03/10/22"},
{"PK_transaction_id":23,"tx":1,"rx":2,"asset":"bnb","value":0.08,"timestamp":"03/11/22"},
{"PK_transaction_id":24,"tx":1,"rx":2,"asset":"bnb","value":-0.01,"timestamp":"03/12/22"},
{"PK_transaction_id":25,"tx":1,"rx":2,"asset":"bnb","value":-0.18,"timestamp":"03/13/22"},
{"PK_transaction_id":26,"tx":1,"rx":2,"asset":"bnb","value":0.10,"timestamp":"03/14/22"},
{"PK_transaction_id":27,"tx":1,"rx":2,"asset":"btc","value":0.09,"timestamp":"03/15/22"},
{"PK_transaction_id":28,"tx":1,"rx":2,"asset":"btc","value":0.14,"timestamp":"03/16/22"},
{"PK_transaction_id":29,"tx":1,"rx":2,"asset":"bnb","value":-0.17,"timestamp":"03/17/22"},
{"PK_transaction_id":30,"tx":1,"rx":2,"asset":"btc","value":-0.10,"timestamp":"03/18/22"},
{"PK_transaction_id":31,"tx":1,"rx":2,"asset":"btc","value":0.18,"timestamp":"03/19/22"},
{"PK_transaction_id":32,"tx":1,"rx":2,"asset":"btc","value":0.02,"timestamp":"03/20/22"},
{"PK_transaction_id":33,"tx":1,"rx":2,"asset":"bnb","value":-0.03,"timestamp":"03/21/22"},
{"PK_transaction_id":34,"tx":1,"rx":2,"asset":"btc","value":-0.07,"timestamp":"03/22/22"},
{"PK_transaction_id":35,"tx":1,"rx":2,"asset":"btc","value":-0.06,"timestamp":"03/23/22"},
{"PK_transaction_id":36,"tx":1,"rx":2,"asset":"btc","value":0.00,"timestamp":"03/24/22"},
{"PK_transaction_id":37,"tx":1,"rx":2,"asset":"btc","value":0.11,"timestamp":"03/25/22"},
{"PK_transaction_id":38,"tx":1,"rx":2,"asset":"eth","value":0.06,"timestamp":"03/26/22"},
{"PK_transaction_id":39,"tx":1,"rx":2,"asset":"btc","value":0.07,"timestamp":"03/27/22"},
{"PK_transaction_id":40,"tx":1,"rx":2,"asset":"eth","value":-0.08,"timestamp":"03/28/22"},
{"PK_transaction_id":41,"tx":1,"rx":2,"asset":"eth","value":0.19,"timestamp":"03/29/22"},
{"PK_transaction_id":42,"tx":1,"rx":2,"asset":"btc","value":0.11,"timestamp":"03/30/22"},
{"PK_transaction_id":43,"tx":1,"rx":2,"asset":"btc","value":-0.18,"timestamp":"03/31/22"},
{"PK_transaction_id":44,"tx":1,"rx":2,"asset":"btc","value":0.08,"timestamp":"04/01/22"},
{"PK_transaction_id":45,"tx":1,"rx":2,"asset":"eth","value":-0.17,"timestamp":"04/02/22"},
{"PK_transaction_id":46,"tx":1,"rx":2,"asset":"bnb","value":0.17,"timestamp":"04/03/22"},
{"PK_transaction_id":47,"tx":1,"rx":2,"asset":"bnb","value":0.14,"timestamp":"04/04/22"},
{"PK_transaction_id":48,"tx":1,"rx":2,"asset":"bnb","value":0.02,"timestamp":"04/05/22"},
{"PK_transaction_id":49,"tx":1,"rx":2,"asset":"btc","value":0.14,"timestamp":"04/06/22"},
{"PK_transaction_id":50,"tx":1,"rx":2,"asset":"bnb","value":0.14,"timestamp":"04/07/22"},
{"PK_transaction_id":51,"tx":1,"rx":2,"asset":"btc","value":-0.05,"timestamp":"04/08/22"},
{"PK_transaction_id":52,"tx":1,"rx":2,"asset":"bnb","value":0.16,"timestamp":"04/09/22"},
{"PK_transaction_id":53,"tx":1,"rx":2,"asset":"bnb","value":0.16,"timestamp":"04/10/22"},
{"PK_transaction_id":54,"tx":1,"rx":2,"asset":"bnb","value":-0.10,"timestamp":"04/11/22"},
{"PK_transaction_id":55,"tx":1,"rx":2,"asset":"btc","value":-0.11,"timestamp":"04/12/22"},
{"PK_transaction_id":56,"tx":1,"rx":2,"asset":"btc","value":0.18,"timestamp":"04/13/22"},
{"PK_transaction_id":57,"tx":1,"rx":2,"asset":"eth","value":0.12,"timestamp":"04/14/22"},
{"PK_transaction_id":58,"tx":1,"rx":2,"asset":"bnb","value":0.10,"timestamp":"04/15/22"},
{"PK_transaction_id":59,"tx":1,"rx":2,"asset":"bnb","value":-0.18,"timestamp":"04/16/22"},
{"PK_transaction_id":60,"tx":1,"rx":2,"asset":"eth","value":-0.01,"timestamp":"04/17/22"},
{"PK_transaction_id":61,"tx":1,"rx":2,"asset":"eth","value":-0.01,"timestamp":"04/18/22"},
{"PK_transaction_id":62,"tx":1,"rx":2,"asset":"bnb","value":0.01,"timestamp":"04/19/22"},
{"PK_transaction_id":63,"tx":1,"rx":2,"asset":"eth","value":-0.07,"timestamp":"04/20/22"},
{"PK_transaction_id":64,"tx":1,"rx":2,"asset":"btc","value":0.06,"timestamp":"04/21/22"},
{"PK_transaction_id":65,"tx":1,"rx":2,"asset":"btc","value":-0.10,"timestamp":"04/22/22"},
{"PK_transaction_id":66,"tx":1,"rx":2,"asset":"eth","value":-0.05,"timestamp":"04/23/22"},
{"PK_transaction_id":67,"tx":1,"rx":2,"asset":"bnb","value":0.04,"timestamp":"04/24/22"},
{"PK_transaction_id":68,"tx":1,"rx":2,"asset":"bnb","value":-0.15,"timestamp":"04/25/22"},
{"PK_transaction_id":69,"tx":1,"rx":2,"asset":"eth","value":-0.04,"timestamp":"04/26/22"},
{"PK_transaction_id":70,"tx":1,"rx":2,"asset":"eth","value":0.14,"timestamp":"04/27/22"},
{"PK_transaction_id":71,"tx":1,"rx":2,"asset":"btc","value":-0.16,"timestamp":"04/28/22"},
{"PK_transaction_id":72,"tx":1,"rx":2,"asset":"eth","value":0.18,"timestamp":"04/29/22"},
{"PK_transaction_id":73,"tx":1,"rx":2,"asset":"eth","value":-0.05,"timestamp":"04/30/22"},
{"PK_transaction_id":74,"tx":1,"rx":2,"asset":"eth","value":-0.08,"timestamp":"05/01/22"},
{"PK_transaction_id":75,"tx":1,"rx":2,"asset":"btc","value":-0.18,"timestamp":"05/02/22"},
{"PK_transaction_id":76,"tx":1,"rx":2,"asset":"eth","value":0.15,"timestamp":"05/03/22"},
{"PK_transaction_id":77,"tx":1,"rx":2,"asset":"eth","value":-0.19,"timestamp":"05/04/22"},
{"PK_transaction_id":78,"tx":1,"rx":2,"asset":"btc","value":0.12,"timestamp":"05/05/22"},
{"PK_transaction_id":79,"tx":1,"rx":2,"asset":"btc","value":-0.06,"timestamp":"05/06/22"},
{"PK_transaction_id":80,"tx":1,"rx":2,"asset":"bnb","value":0.05,"timestamp":"05/07/22"},
{"PK_transaction_id":81,"tx":1,"rx":2,"asset":"bnb","value":-0.09,"timestamp":"05/08/22"},
{"PK_transaction_id":82,"tx":1,"rx":2,"asset":"btc","value":0.12,"timestamp":"05/09/22"},
{"PK_transaction_id":83,"tx":1,"rx":2,"asset":"btc","value":-0.05,"timestamp":"05/10/22"},
{"PK_transaction_id":84,"tx":1,"rx":2,"asset":"bnb","value":0.10,"timestamp":"05/11/22"},
{"PK_transaction_id":85,"tx":1,"rx":2,"asset":"bnb","value":-0.12,"timestamp":"05/12/22"},
{"PK_transaction_id":86,"tx":1,"rx":2,"asset":"bnb","value":0.04,"timestamp":"05/13/22"},
{"PK_transaction_id":87,"tx":1,"rx":2,"asset":"bnb","value":-0.03,"timestamp":"05/14/22"},
{"PK_transaction_id":88,"tx":1,"rx":2,"asset":"bnb","value":0.09,"timestamp":"05/15/22"},
{"PK_transaction_id":89,"tx":1,"rx":2,"asset":"btc","value":0.11,"timestamp":"05/16/22"},
{"PK_transaction_id":90,"tx":1,"rx":2,"asset":"eth","value":0.07,"timestamp":"05/17/22"},
{"PK_transaction_id":91,"tx":1,"rx":2,"asset":"eth","value":-0.06,"timestamp":"05/18/22"},
{"PK_transaction_id":92,"tx":1,"rx":2,"asset":"btc","value":-0.14,"timestamp":"05/19/22"},
{"PK_transaction_id":93,"tx":1,"rx":2,"asset":"eth","value":0.04,"timestamp":"05/20/22"},
{"PK_transaction_id":94,"tx":1,"rx":2,"asset":"bnb","value":0.20,"timestamp":"05/21/22"},
{"PK_transaction_id":95,"tx":1,"rx":2,"asset":"eth","value":-0.07,"timestamp":"05/22/22"},
{"PK_transaction_id":96,"tx":1,"rx":2,"asset":"bnb","value":0.20,"timestamp":"05/23/22"},
{"PK_transaction_id":97,"tx":1,"rx":2,"asset":"btc","value":0.01,"timestamp":"05/24/22"},
{"PK_transaction_id":98,"tx":1,"rx":2,"asset":"eth","value":-0.10,"timestamp":"05/25/22"},
{"PK_transaction_id":99,"tx":1,"rx":2,"asset":"bnb","value":-0.07,"timestamp":"05/26/22"}]


c = initexithandler.core['LedgerClient'].LedgerClient()
dates = pd.date_range(datetime(2022,2,17), datetime(2022,5,28))

for i, d in enumerate(sqldata):
    print(d["PK_transaction_id"], sep='\t')
    c.do_ledger_transaction(3, d['rx'], d['asset'],d['value'])
    c._mysql_update('transactions', ["timestamp"], [dates[i]],
                    ["PK_transaction_id", 99+int(d["PK_transaction_id"])])

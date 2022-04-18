import logging

from lib.core import initexit
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(filename='/home/common/dev/logs/zephyr.log', level=logging.DEBUG)

initexithandler = initexit.initexit()
initexithandler.import_dependencies()
initexithandler.exit()
initexithandler.init()
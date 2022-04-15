import subprocess
import logging
import os
import time

from dotenv import load_dotenv

logging.basicConfig(filename='/home/common/dev/logs/zephyr.log', level=logging.DEBUG)
load_dotenv('/home/common/dev/.env')


# Ganache local ethereum blockchain
class Ganache:
    def __init__(self):
        logging.debug('initializing Ganache')
        # get ganache data dir from .env
        self.datadir = os.environ.get('GANACHE_DATADIR')
        # port that ganache runs on
        self.port = os.environ.get('GANACHE_PORT')
        # get absolute path of executable
        _executable = os.environ.get('GANACHE_EXECUTABLE')
        _executable = subprocess.check_output(['bash', 'which', _executable])
        self.executable = _executable.decode("utf-8").rstrip('\n')

    def start(self):
        # --db flag sets datadir
        _startcommand = [self.executable, '--db', self.datadir]
        # start ganache and detach
        subprocess.Popen(_startcommand, start_new_session=True)
        logging.debug('started Ganache')

    def stop(self):
        try:
            # get pid of ganache process
            _pid = subprocess.check_output(['lsof', '-t', '-i:' + self.port]).decode("utf-8").rstrip('\n')
            _stopcommand = ['kill', '-9', _pid]
            # kill ganache process
            subprocess.check_output(_stopcommand).decode("utf-8")
            logging.debug('stopped Ganache')
        except subprocess.CalledProcessError as e:
            logging.debug('Ganache failed to stop or is not started: {}'.format(e))

# g = Ganache()
# g.start()
# time.sleep(15)
# g.stop()
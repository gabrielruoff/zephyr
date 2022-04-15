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
        self.pid = None

    def _detect_running(self):
        try:
            # get pid of ganache process
            self.pid = subprocess.check_output(['lsof', '-t', '-i:' + self.port]).decode("utf-8").rstrip('\n')
            logging.debug('Ganache is running ({})'.format(self.pid))
            return True
        except subprocess.CalledProcessError as e:
            logging.debug('Ganache is not running')
        return False

    def start(self):
        # --db flag sets datadir
        _startcommand = [self.executable, '--db', self.datadir]
        # start ganache and detach
        subprocess.Popen(_startcommand, start_new_session=True)
        logging.debug('started Ganache')

    def stop(self):
        logging.debug('Stopping Ganache')
        if self._detect_running():
            try:
                _stopcommand = ['kill', '-9', self.pid]
                # kill ganache process
                subprocess.check_output(_stopcommand).decode("utf-8")
                logging.debug('stopped Ganache ({})'.format(self.pid))
            except subprocess.CalledProcessError as e:
                 logging.debug('Ganache failed to stop or is not started: {}'.format(e))
        else:
            logging.debug('Cannot stop. Ganache is not running')

# g = Ganache()
# g.stop()
# g.start()
# time.sleep(15)
# g.stop()
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
        self.keyspath = os.environ.get('GANACHE_KEYSPATH')
        self.mnemonic = os.environ.get('GANACHE_MNEMONIC')
        # port that ganache runs on
        self.port = os.environ.get('GANACHE_PORT')
        # get absolute path of executable
        _executable = os.environ.get('GANACHE_EXECUTABLE')
        _executable = subprocess.check_output(['bash', 'which', _executable])
        self.executable = _executable.decode("utf-8").rstrip('\n')
        self.pid = None

    def __enter__(self):
        self.__init__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

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
        logging.debug('Starting Ganache')
        if not self._detect_running():
            # --db flag sets datadir
            _startcommand = [self.executable, '--db', self.datadir, '--account_keys_path', self.keyspath, '-m', self.mnemonic]
            # start ganache and detach process
            subprocess.Popen(_startcommand, start_new_session=True)
            logging.debug('Started Ganache')
            logging.debug('Waiting for ganache to start...')
            while not self._detect_running():
                time.sleep(0.2)
            logging.debug('Confirmed Ganache has started')
        else:
            logging.debug('Not starting Ganache, already started')

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
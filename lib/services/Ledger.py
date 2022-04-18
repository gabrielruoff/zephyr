import logging
import os
import docker
from dotenv import load_dotenv

logging.basicConfig(filename='/home/common/dev/logs/zephyr.log', level=logging.DEBUG)
load_dotenv('/home/common/dev/.env')


class Ledger:
    def __init__(self):
        logging.debug('initializing ledger')
        self.confdir = os.environ.get('LEDGER_CONF_DIR')
        self.datadir = os.environ.get('LEDGER_DATADIR')
        self.docker = docker.from_env()
        self.containername = 'ledger'
        self.imagename = os.environ.get('LEDGER_DOCKER_IMAGE')
        self.port = os.environ.get('LEDGER_PORT')
        self.passwd = os.environ.get('LEDGER_PASS')
        self.ledger = None
        self._detect_running()

    def __enter__(self):
        self.__init__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.docker.close()

    def _detect_running(self):
        try:
            self.ledger = self.docker.containers.get(self.containername)
            logging.debug('ledger already running, attaching...')
            return True
        except docker.errors.NotFound as e:
            logging.debug('ledger not already running')
        return False

    def start(self):
        logging.debug('starting ledger')
        _volumes = ['{}:{}'.format(self.confdir, '/etc/mysql'), '{}:{}'.format(self.datadir, '/var/lib/mysql')]
        _ports = {'3306/tcp': int(self.port)}
        _environment = ['MYSQL_ROOT_PASSWORD={}'.format(self.passwd)]
        if not self._detect_running():
            try:
                self.ledger = self.docker.containers.run(self.imagename, name=self.containername,
                                                         hostname=self.containername, volumes=_volumes, ports=_ports,
                                                         environment=_environment, detach=True)
            except docker.errors.APIError as e:
                raise Warning('failed to start ledger: {}'.format(e))
        else:
            logging.debug('Not starting Ledger, already started')

    def stop(self):
        logging.debug('stopping ledger')
        if self.ledger is None:
            logging.debug('cannot stop. ledger is not running')
            return
        try:
            self.ledger.stop()
            self.ledger.remove()
        except docker.errors.APIError as e:
            logging.debug('failed to stop ledger: {}'.format(e))



# l = Ledger()
# l.start()
# time.sleep(60)
# l.stop()

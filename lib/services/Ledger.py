import logging
import os
import time
import mysql.connector

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
        self.ledger = None
        self._detect_running()

    def _detect_running(self):
        try:
            self.ledger = self.docker.containers.get(self.containername)
            logging.debug('ledger already running, attaching...')
        except docker.errors.NotFound as e:
            logging.debug('ledger not already running')

    def Start(self):
        logging.debug('starting ledger')
        _volumes = ['{}:{}'.format(self.confdir, '/etc/mysql'), '{}:{}'.format(self.datadir, '/var/lib/mysql')]
        _ports = {'{}/tcp'.format(self.port): int(self.port) + 1}
        _environment = ['MYSQL_ROOT_PASSWORD=zephyr']
        try:
            self.ledger = self.docker.containers.run(self.imagename, name=self.containername,
                                                     hostname=self.containername, volumes=_volumes, ports=_ports,
                                                     environment=_environment, detach=True)
        except docker.errors.APIError as e:
            raise Warning('failed to start ledger: {}'.format(e))

    def Stop(self):
        logging.debug('stopping ledger')
        if self.ledger is None:
            logging.debug('cannot stop. ledger is not running')
            return
        try:
            self.ledger.stop()
            self.ledger.remove()
        except docker.errors.APIError as e:
            logging.debug('failed to stop ledger: {}'.format(e))


class ledger_client:
    def __init__(self):
        self.host = os.environ.get('LEDGER_HOST')
        self.user = os.environ.get('LEDGER_USER')
        self.port = os.environ.get('LEDGER_PORT')
        self.db = os.environ.get('LEDGER_DB')
        self.cnx = mysql.connector.connect(user=self.user, host=self.host, database=self.db)


# l = Ledger()
# l.Start()
# time.sleep(60)
# l.Stop()

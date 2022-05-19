import configparser
import logging
import os
import sys
import time
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(filename='/home/common/dev/logs/zephyr.log', level=logging.DEBUG)


class initexit:
    def __init__(self):
        # get path to conf file
        conf_zephyr = os.environ.get('PATH_CONF')
        # initialize config reader
        self.config = configparser.RawConfigParser()
        self.config.read(conf_zephyr)

        # uninitialized
        self.dependencies = {}
        self.services = {}
        self.core = {}

    def __enter__(self):
        self.__init__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def import_dependencies(self):
        logging.debug('Importing dependencies')
        # read dependencies
        dependencies = dict(self.config.items('Dependencies'))
        # services
        self.dependencies['services'] = dependencies['services'].split(',')
        # core
        self.dependencies['core'] = dependencies['core'].split(',')
        # import dependencies
        # services
        # add services dir to path
        sys.path.insert(1, os.environ.get('PATH_SERVICES'))
        # import services
        _values = list(map(__import__, self.dependencies['services']))
        for i, key in enumerate(self.dependencies['services']):
            self.services[key] = _values[i]
        # for i, s in enumerate(self.dependencies['services']):
        #     sys.modules.append(_modules[i])
        # core
        # add clients dir to path
        sys.path.insert(1, os.environ.get('PATH_CORE'))
        # import core
        _values = list(map(__import__, self.dependencies['core']))
        for i, key in enumerate(self.dependencies['core']):
            self.core[key] = _values[i]

    def init(self, check=True):
        logging.debug('Running init')
        if not self.dependencies:
            raise Warning('Trying to init without importing dependencies')
        # start all services
        for service in self.dependencies['services']:
            logging.debug('Starting {}'.format(service))
            _module = sys.modules[service]
            with getattr(_module, service)() as s:
                s.start()
        logging.debug('Init OK')
        if check:
            self._init_check()

    def _init_check(self):
        # check services have been started
        logging.debug('Running init check')
        for service in self.dependencies['services']:
            _module = sys.modules[service]
            with getattr(_module, service)() as s:
                if not s._detect_running():
                    raise Warning('Service {} is not running'.format(service))
        logging.debug('Init check OK')

    def exit(self, check=True):
        logging.debug('Running exit')
        # stop all services
        for service in self.dependencies['services']:
            logging.debug('Stopping {}'.format(service))
            _module = sys.modules[service]
            with getattr(_module, service)() as s:
                s.stop()
        logging.debug('Exit OK')
        if check:
            self.exit_check()

    def exit_check(self):
        # check services have stopped
        logging.debug('Running exit check')
        for service in self.dependencies['services']:
            _module = sys.modules[service]
            with getattr(_module, service)() as s:
                if s._detect_running():
                    raise Warning('Service {} is still running'.format(service))
        logging.debug('Exitcheck OK')

# i = initexit()
# i.import_dependencies()
# i.init()
# i.init_check()
# time.sleep(5)
# i.exit()
# i.exit_check()
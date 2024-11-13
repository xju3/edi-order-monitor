import logging

from common.app_config import AppConfig
from common.db import DBEngine
from utils.log import init_logger


class Env(object):
    _instance = None

    _context = None
    _config = None
    _logger = None
    _session = None
    _tasks = 0

    def __new__(cls, *args, **kw):
        if not cls._instance:
            cls._instance = super(Env, cls).__new__(cls, *args, **kw)
        return cls._instance

    def init(self, ctx):
        self._context = ctx
        settings = ctx.get_resource('settings.ini')
        self._config = AppConfig(settings).load()
        db_engine = DBEngine(self._config)
        self._session = db_engine.get_session()
        logger_root = 'root'
        logger_file = '/var/tmp/pul-monitor.{0}.log'
        init_logger(logger_root, logger_file)
        self._logger = logging.getLogger(logger_root)

    @property
    def tasks(self):
        return self._tasks

    @tasks.setter
    def tasks(self, x):
        self._tasks = x

    @property
    def context(self):
        return self._context

    @property
    def config(self):
        return self._config

    @property
    def session(self):
        return self._session

    @property
    def logger(self):
        return logging.getLogger('root')

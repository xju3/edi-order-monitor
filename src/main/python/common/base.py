# coding: utf-8

from env import Env


class Base(object):
    env = Env()
    config = env.config
    context = env.context
    logger = env.logger
    session = env.session

    def __init__(self):
        pass


class Singleton(Base):
    _instance = None

    def __new__(cls, *args, **kw):
        if not cls._instance:
            cls._instance = super(Singleton, cls).__new__(cls, *args, **kw)
        return cls._instance

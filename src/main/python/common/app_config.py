# coding: utf-8


from configparser import RawConfigParser


class AppConfig(object):

    def __init__(self, confg_file):
        super(AppConfig).__init__()
        self._config_file = confg_file
        self.config = {}

    def load(self):
        config = RawConfigParser()
        config.read(self._config_file)
        return config

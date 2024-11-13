# coding: utf-8

import requests
import logging

from common.base import Singleton


class WebFetcher(Singleton):
    logger = logging.getLogger("root")

    def __init__(self):
        super().__init__()
        self.s = requests.session()

    def form_get(self, url):
        return self.s.get(url)

    def form_request(self, url, params):
        return self.s.post(url, data=params)

    def json_request(self, url, data):
        return self.s.post(url, json=data)

    def downlaod(self, url):
        return self.s.get(url)

import json
import time
from time import sleep
from common.base import Base
from common.web_fetcher import WebFetcher
from exception.pul_exception import DocumentNotReadyException
from domain.handler.xls_handler import XlsHandler
from utils.http import ok

fetcher = WebFetcher()


def document_ready(url):
    res = fetcher.form_get(url)
    if ok(res.status_code):
        content = json.loads(res.content)
        return content['documentReady']
    return False


class XlsSpider(Base):

    def __init__(self, pul_master, items_count):
        super(XlsSpider).__init__()
        self.pul_master = pul_master
        self.xls_header = self.context.get_resource('xls_header.json')
        self.xls_item = self.context.get_resource("xls_item.json")
        # self.logger.debug(self.xls_header)
        self._host = self.config.get('app', 'domain')
        self.items_count = items_count

    def exec(self):
        self.report()

    def report(self):
        try:
            url = self.config.get('report', 'url')
            url = url.format(self.pul_master.ShipmentId)
            self.logger.debug(url)
            res = fetcher.form_get(self._host + url)
            if ok(res.status_code):
                client_id, instance_id, document_id = self.get_ids()
                self.check(client_id, instance_id, document_id)
            else:
                self.logger.error("failed get report.")
        except Exception as e:
            self.logger.error(e)
            raise e

    def check(self, client_id, instance_id, document_id):
        url = self.config.get('check', "url")
        url = url.format(client_id, instance_id, document_id)
        url = self._host + url
        self.logger.debug(url)
        ready = False
        times = 0
        while not ready:
            times += 1
            sleep(1)
            self.logger.debug("document not ready")
            ready = document_ready(url)
            if times == 10:
                raise DocumentNotReadyException("document always not ready, curr task will be aborded")

        self.get_excel(client_id, instance_id, document_id)

    def get_documenet_id(self, client_id, instance_id):
        url = self.config.get('document', 'url')
        url = url.format(client_id, instance_id)
        self.logger.debug(url)
        params = self.config.get('document', 'params')
        res = fetcher.json_request(self._host + url, json.loads(params))
        if ok(res.status_code):
            data = json.loads(res.content)
            document_id = data['documentId']
            self.logger.debug("document id: %s" % document_id)
            return document_id
        else:
            self.logger.error("failed get document id")
        return None

    def get_excel(self, client_id, instance_id, document_id):
        url = self.config.get('download', 'url')
        url = url.format(client_id, instance_id, document_id)
        self.logger.debug(url)
        res = fetcher.downlaod(self._host + url)
        if ok(res.status_code):
            xls_handler = XlsHandler(self.pul_master, res.content, self.items_count)
            xls_handler.exec()
        else:
            self.logger.debug('get excel failed: {0}' % res.status_code)

    def get_instance_id(self, client_id, pul_no):
        url = self.config.get('instance', 'url')
        params = self.config.get('instance', 'params')
        ex = self.config.get('instance', 'ex')
        ex = ex.replace("PUL_CODE", pul_no)
        url = url.format(client_id)
        self.logger.debug(url)
        params = params.replace("PUL_CODE", pul_no)
        params = json.loads(params)
        params['report'] = ex
        params = json.dumps(params)
        params.replace("'", "\"")
        # self.logger.debug(params)
        res = fetcher.json_request(self._host + url, json.loads(params))
        if ok(res.status_code):
            data = json.loads(res.content)
            instance_id = data['instanceId']
            self.logger.debug("instance id: %s" % instance_id)
            document_id = self.get_documenet_id(client_id, instance_id)
            return client_id, instance_id, document_id
        else:
            self.logger.error("no instance id")
        return None, None, None

    def get_ids(self):
        url = self.config.get("clients", "url");
        params = self.config.get("clients", 'params')
        params = json.loads(params)
        params['timestamp'] = time.time() * 1000
        self.logger.debug(url)
        res = fetcher.json_request(self._host + url, params)
        if ok(res.status_code):
            data = json.loads(res.content)
            client_id = data['clientId']
            return self.get_instance_id(client_id, self.pul_master.ShipmentId)
        return None, None, None

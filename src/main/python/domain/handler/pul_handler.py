#!/usr/bin/env python
# coding: utf-8

import json
from domain.dao.pul_dao import PulDao
from domain.handler.base_handler import BaseHandler
from spider.xls_spider import XlsSpider
from utils.mail_util import MailUtil


class PulHandler(BaseHandler):

    def __init__(self, data, callback, pul_log):
        super(PulHandler).__init__()
        self.callback = callback
        self.pul_log = pul_log
        self.data = json.loads(data)
        # self.logger.debug(self.data)
        self.dao = PulDao(self.callback, self.pul_log)
        self.email = MailUtil()

    def exec_callback(self, text):
        if self.callback:
            self.callback(text)

    def exec(self):
        success = self.data['success']
        # self.logger.debug(success)
        if not success:
            self.exec_callback("failed")
            self.logger.error("fetch data failed")
            return

        items = self.data['data']
        self.pul_log.total = len(items)
        self.exec_callback("pul items: {0}".format(len(items)))
        # logger.debug(items)

        for item in items:

            try:
                # logger.debug(item)
                shipment_id = item['ShipmentId']
                status = item['ShipmentTypeStatusText']
                if status == 'Delivered':
                    self.pul_log.delivered += 1
                    # self.logger.debug("{0}: delivered" % shipment_id)
                    self.exec_callback("pul:{0} has been delivered".format(shipment_id))
                    continue
                xls_spider = None

                master = self.dao.get_pul_master(shipment_id)
                if master is None:
                    self.pul_log.fresh_item += 1
                    master, items_count = self.dao.save_pul(item)
                    # logger.debug(master)
                    # self.logger.debug(items_count)
                    xls_spider = XlsSpider(master, items_count)
                else:
                    revision = item['PULRevisionNumber']
                    if master.PULRevisionNumber == revision:
                        # self.logger.debug("{0}: revision duplicated" % shipment_id)
                        self.pul_log.revision_duplicated += 1
                        # self.logger.debug("shipmentId: {0} revision {1}
                        # is same as before".format(master.ShipmentId, master.PULRevisionNumber))
                    else:
                        self.logger.debug("revision changed")
                        self.pul_log.revision_changed += 1
                        master.Available = 0
                        # self.dao.del_pul(master.ShipmentId)
                        master, items_count = self.dao.save_pul(item)
                        xls_spider = XlsSpider(master, items_count)
                        # 对于有新的修订版本的暂不删除，只做标记
                if xls_spider is not None:
                    xls_spider.exec()
                    self.logger.debug("start xls spider.")
                else:
                    self.logger.debug("xls spider is None, skipped")
            except Exception as e:
                self.logger.debug(e)
                raise e

        self.dao.save_pul_log(self.pul_log)
        self.email.send_pul_log(self.pul_log)

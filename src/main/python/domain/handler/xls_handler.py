# coding: utf-8

import xlrd
import json

from domain.handler.base_handler import BaseHandler
from domain.model.model import XlsHeader, XlsItem


def get_column_index(code):
    count = len(code)
    index = 0
    for c in code:
        count -= 1
        index += (ord(c) - 64) * pow(26, count)
    return index - 1


def get_start(sheet):
    start = 47
    val = str(sheet.cell_value(2, start))
    if val is not None and len(val) > 0:
        return start
    return start + 1


class XlsHandler(BaseHandler):

    def __init__(self, pul_master, content, items_count):
        super(XlsHandler).__init__()
        self.pul_master = pul_master
        self.xls_header = self.env.context.get_resource('xls_header.json')
        self.xls_item = self.env.context.get_resource('xls_item.json')
        self.item_count = items_count
        with open(self.xls_header) as file:
            self.xls_header = json.load(file)

        with open(self.xls_item) as file:
            self.xls_item = json.load(file)

        self.save_excel(content)

        # self.xls = xlrd.open_workbook(file_contents=content, logfile=open(os.devnull, 'w'))
        self.xls = xlrd.open_workbook(file_contents=content)

    def save_excel(self, content):
        local = bool(self.config.get('excel', 'local'))
        if local:
            path = self.config.get('excel', 'path')
            file_name = path + self.pul_master.ShipmentId + ".xls"
            f = open(file_name, 'wb')
            f.write(content)
            f.close()

    def exec(self):
        try:
            sheet = self.xls.sheet_by_index(0)
            header = self.save_header(sheet)
            self.save_items(header, sheet)
        except Exception as e:
            self.logger.debug(e)
            raise e

    def save_items(self, header, sheet):
        start = get_start(sheet)
        # self.logger.debug("items start from : {0}".format(start))
        step = self.xls_item['step']
        columns = self.xls_item['columns']
        i = 0
        while i < self.item_count:
            xls_item = XlsItem()
            xls_item.header_id = header.Id
            row = start + i * step
            for column in columns:
                # self.logger.debug(column)
                for key in column:
                    value = column[key]
                    column_code = value['code']
                    offset = int(value['offset'])
                    column_index = get_column_index(column_code)
                    cell_value = sheet.cell_value(row + offset - 1, column_index)
                    setattr(xls_item, key, cell_value)
            self.session.add(xls_item)
            i += 1

    def save_header(self, sheet):
        xls_header = XlsHeader()
        for key in self.xls_header:
            value = self.xls_header[key]
            # self.logger.debug(value)
            cell = value['cell']
            replacement = value['replacement']
            cell = cell.split(',')
            column = get_column_index(cell[0])
            row = int(cell[1]) - 1
            cell_value = str(sheet.cell_value(row, column))
            if len(replacement) > 0:
                cell_value = cell_value.replace(replacement, '')
            setattr(xls_header, key, cell_value)
        self.session.add(xls_header)
        return xls_header

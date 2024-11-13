#!/usr/bin/env python
# coding: utf-8

import sys
from sqlalchemy import *
from sqlalchemy.orm import *

from domain.model.model import PulMaster, PulDetail, PulLog, XlsHeader, XlsItem


class DBEngine(object):
    # initialize paramters which used for db connection

    session = None

    def __init__(self, config):
        super(DBEngine).__init__()
        database = config.get('db', 'server')
        self.conn = config.get(database, "conn")
        self.user = config.get(database, 'user')
        self.password = config.get(database, 'password')
        self.host = config.get(database, 'host')
        self.port = config.get(database, 'port')
        self.db = config.get(database, 'db')

    # create db engine
    def __create_engine(self):
        url = self.conn % (self.user, self.password, self.host, self.port, self.db)
        try:
            db_engine = create_engine(url, connect_args={'charset': 'utf8'}, echo=False)
            PulMaster.__table__.create(bind=db_engine, checkfirst=True)
            PulDetail.__table__.create(bind=db_engine, checkfirst=True)
            PulLog.__table__.create(bind=db_engine, checkfirst=True)
            XlsHeader.__table__.create(bind=db_engine, checkfirst=True)
            XlsItem.__table__.create(bind=db_engine, checkfirst=True)
            return db_engine
        except Exception as e:
            print('fetal error encounted', e)
            sys.exit()

    # return session for client
    def get_session(self):
        if self.session is None:
            return scoped_session(sessionmaker(bind=self.__create_engine()))()
        return self.session

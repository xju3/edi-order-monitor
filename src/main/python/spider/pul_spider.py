import json

from common.base import Base
from domain.handler.pul_handler import PulHandler
from domain.model.model import PulLog
from exception.pul_exception import LoginFailedException, FetchJsonDataException
from utils.dt import get_day_offset
from utils.encryption import *
from utils.http import ok
from common.web_fetcher import WebFetcher

fetcher = WebFetcher()


class PulSpider(Base):
    pul_log = PulLog()

    def __init__(self, callback):
        super(PulSpider).__init__()
        self._host = self.config.get('app', 'domain')
        self.callback = callback

    def _login(self):
        self._login_path = self.config.get('login', 'path')
        self.exec_callback("doing login")
        url = self._host + self._login_path
        self.logger.debug(url)
        user_name = self.config.get("login", "user_name")
        password = self.config.get('login', 'password')
        password = md5(password)
        params = {'UserName': user_name, 'Password': password, 'PlainPassword': password}
        res = fetcher.form_request(url, params)
        if not ok(res.status_code):
            raise LoginFailedException("login failed")
        self.pul_log.log_in_status = 1

    def _query(self):
        self.exec_callback("quering data")
        self._query_path = self.config.get('query', 'path')
        self._query_params = self.config.get('query', 'params')
        self._after = self.config.get('query', 'after')
        self._before = self.config.get('query', 'before')
        url = self._host + self._query_path
        self.logger.debug(url)
        start_day = get_day_offset(int(self._before) * -1)
        end_day = get_day_offset(int(self._after))
        params = json.loads(self._query_params)
        params['request']['filter']['filters'][0]['value'] = start_day + "~" + end_day
        params['request']['filter']['filters'][0]['text'] = start_day + "~" + end_day
        # self.logger.debug(params)
        res = fetcher.json_request(url, params)
        if ok(res.status_code):
            self.pul_log.query_status = 1
            return res.content
        else:
            raise FetchJsonDataException('faild to fetch json data')

    def exec(self):
        if self.env.tasks > 0:
            self.logger.debug("A runing task is not completed, skipped.")
            return
        try:
            self.env.tasks += 1
            self.pul_log = PulLog()
            self._login()
            data = self._query()
            # self.logger.debug("pul handler")
            handler = PulHandler(data=data, callback=self.callback, pul_log=self.pul_log)
            handler.exec()
            self.env.session.commit()
        except Exception as e:
            self.env.session.rollback()
            self.logger.error(e)
        finally:
            self.env.tasks -= 1

    def exec_callback(self, text):
        if self.callback:
            self.callback(text)

# coding: utf-8
import sys
from datetime import datetime

from apscheduler.schedulers.qt import QtScheduler
from apscheduler.triggers.interval import IntervalTrigger
from fbs_runtime.application_context.PyQt5 import ApplicationContext
from env import Env


def job(callback):
    env.logger.debug("starting job: {0}".format(datetime.now()))
    from spider.pul_spider import PulSpider
    spider = PulSpider(callback)
    spider.exec()


def set_schedule(minutes, callback):
    from tzlocal import get_localzone
    tz = get_localzone()
    now = datetime.now(tz=tz)
    scheduler = QtScheduler()
    trigger = IntervalTrigger(seconds=minutes, start_date=now)
    scheduler.add_job(lambda: job(callback), trigger)
    scheduler.start()


def init(_logger):
    # main window
    from ui.window import MainWindow
    window = MainWindow()
    # task schedule
    interval = env.config.get('schedule', 'interval')
    _logger.debug('interval: {0}'.format(interval))
    set_schedule(int(interval), window.update_status_bar_text)

    return window


if __name__ == '__main__':
    context = ApplicationContext()
    env = Env()
    env.init(context)
    logger = env.logger
    main_window = init(logger)
    main_window.show()
    exit_code = context.app.exec_()
    sys.exit(context)
